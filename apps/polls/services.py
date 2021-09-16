from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.generics import get_object_or_404

from .models import (
    Poll,
    Answer,
    Question,
    UserAnswer,
    UserQuestionResponse,
    UserPollResponse,
)
from apps.users.services import create_anonymous_user


User = get_user_model()


@transaction.atomic
def create_poll(*, poll_data: dict, questions_data: list) -> Poll:
    """
    Создание опроса и связанных с ним моделей вопросов и ответов.
    """
    poll_obj = Poll.objects.create(**poll_data)

    question_line_number = 0
    for question_data in questions_data:
        question_line_number += 1
        answers_data = question_data.pop("answers", [])
        question_obj = Question.objects.create(
            **question_data, poll=poll_obj, number=question_line_number
        )

        answer_line_number = 0
        for answer_data in answers_data:
            answer_line_number += 1
            Answer.objects.create(
                **answer_data, question=question_obj, number=answer_line_number
            )

    return poll_obj


@transaction.atomic
def update_poll(*, poll_instance: Poll, poll_data: dict, questions_data: list) -> Poll:
    """
    Обновление опроса и связанных с ним моделей вопросов и ответов.
    """

    for attr, value in poll_data.items():
        setattr(poll_instance, attr, value)

    poll_instance.save()

    question_line_number = 0
    for question_data in questions_data:
        question_line_number += 1
        answers_data = question_data.pop("answers", [])
        question_obj, created = Question.objects.get_or_create(
            defaults=dict(**question_data),
            poll=poll_instance,
            number=question_line_number,
        )

        if not created:
            question_obj.question_text = question_data["question_text"]
            question_obj.question_type = question_data["question_type"]
            question_obj.save()

        answer_line_number = 0
        for answer_data in answers_data:
            answer_line_number += 1
            answer_obj, created = Answer.objects.get_or_create(
                defaults=dict(**answer_data),
                question=question_obj,
                number=answer_line_number,
            )

            if not created:
                answer_obj.text = answer_data["text"]
                answer_obj.save()

        question_obj.answers.filter(number__gt=answer_line_number).delete()

    poll_instance.questions.filter(number__gt=question_line_number).delete()

    return poll_instance


@transaction.atomic
def create_vote(*, data: dict, user: User, poll_id: int):
    """
    Создание ответа на вопрос.
    """
    poll = get_object_or_404(Poll, id=poll_id)
    
    # если пользователь не авторизован, то создаём анонимного пользователя
    if not user.is_authenticated:
        user = create_anonymous_user()
        
    user_poll_response, _ = UserPollResponse.objects.get_or_create(user=user, poll=poll)

    for chunk in data:
        question = chunk["question"]
        answers = chunk.get("answers", [])
        answer_text = chunk.get("answer_text", "")

        question_response = UserQuestionResponse.objects.create(
            user_poll_response=user_poll_response,
            user=user,
            question=question,
            answer_text=answer_text,
        )

        for answer in answers:
            UserAnswer.objects.create(
                answer=answer,
                user_question_response=question_response,
            )
            if answer:
                answer.votes_qty += 1
                answer.save()
