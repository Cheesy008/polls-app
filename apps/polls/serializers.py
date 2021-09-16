from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Poll, Answer, Question, UserAnswer
from .services import create_poll, create_vote, update_poll


User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "number",
            "text",
            "votes_qty",
        )
        read_only_fields = (
            "number",
            "votes_qty",
        )


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = (
            "id",
            "number",
            "question_text",
            "question_type",
            "answers",
        )
        read_only_fields = ("number",)


class PollSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания, редактирования и вывода деталей опроса.
    """

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "created_by",
            "questions",
        )
        read_only_fields = ("created_by",)

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        poll = create_poll(
            poll_data=validated_data,
            questions_data=questions_data,
        )
        return poll

    def update(self, instance, validated_data):
        if instance.has_votes:
            raise ValidationError(
                {"error": "Вы не можете изменить опрос, т.к. в нём уже проголосовали"}
            )

        questions_data = validated_data.pop("questions", [])
        poll = update_poll(
            poll_instance=instance,
            poll_data=validated_data,
            questions_data=questions_data,
        )
        return poll


class PollListSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода списка опросов.
    """

    class Meta:
        model = Poll
        fields = (
            "id",
            "title",
            "start_date",
            "end_date",
            "created_by",
        )
        read_only_fields = ("__all__",)


class SendUserAnswerSerializer(serializers.Serializer):
    """
    Сериалайзер для отправки ответов на вопрос.
    """

    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Answer.objects.all(), required=False
    )
    answer_text = serializers.CharField(required=False)

    def validate(self, attrs):
        question = attrs["question"]
        answers = attrs.get("answers", [])
        answer_text = attrs.get("answer_text", None)
        poll_id = self.context["poll_id"]

        poll = Poll.objects.find_active_by_id(poll_id).first()
        if not poll:
            raise ValidationError({"error": "Опрос не был найден в списке активных"})

        question_id = question.id

        if not poll.questions.filter(id=question_id).exists():
            raise ValidationError(
                {"error": f"Вопроса с id {question_id} не существует"}
            )

        if (
            question.question_type in [Question.SINGLE, Question.MULTIPLE]
            and answer_text
        ):
            ValidationError(
                {"error": f"Вопрос с id {question_id} не может иметь ответ текстом"}
            )

        if question.question_type == Question.SINGLE and len(answers) > 1:
            raise ValidationError(
                {
                    "error": f"Вопрос с id {question_id} может иметь только один вариант ответа"
                }
            )

        if question.question_type == Question.TEXT and answers:
            raise ValidationError(
                {"error": f"Вопрос с id {question_id} может иметь только ответ текстом"}
            )

        for answer in answers:
            if answer and not question.answers.filter(id=answer.id).exists():
                raise ValidationError(
                    {"error": f"Ответа с id {answer.id} не существует"}
                )

        return attrs
