import pytz
from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError


class PollManager(models.Manager):
    def active_polls(self):
        """
        Возвращает queryset активных опросов.
        """
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        return self.get_queryset().filter(end_date__gt=utc_now)


class Poll(models.Model):
    """
    Модель опроса.
    """

    title = models.CharField("Название", max_length=225)
    description = models.TextField("Описание")
    start_date = models.DateTimeField("Время начала опроса")
    end_date = models.DateTimeField("Время окончания опроса")
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="polls",
        verbose_name="Пользователь",
    )

    objects = PollManager()

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    @property
    def has_votes(self):
        """
        Голосовал ли кто то в опросе.
        """
        for question in self.questions.all():
            for answer in question.answers.all():
                if answer.votes_qty > 0:
                    return True
        else:
            return False

    def clean(self) -> None:
        if self.start_date > self.end_date:
            raise ValidationError(
                {"error": "Дата начала не может быть больше даты окончания опроса"}
            )

        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save()


class Question(models.Model):
    """
    Модель вопроса.
    """

    TEXT = "TE"  # ответ текстом
    SINGLE = "SI"  # ответ с выбором одного варианта
    MULTIPLE = "MU"  # ответ с выбором нескольких вариантов

    QUESTION_TYPE_CHOICES = (
        (TEXT, "Text"),
        (SINGLE, "Single"),
        (MULTIPLE, "Multiple"),
    )

    number = models.PositiveIntegerField("Номер", default=1)
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="questions", verbose_name="Опрос"
    )
    question_text = models.TextField("Текст вопроса")
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=SINGLE,
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    """
    Модель ответа.
    """

    number = models.PositiveIntegerField("Номер", default=1)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    text = models.TextField("Ответ")
    votes_qty = models.PositiveIntegerField("Количество голосов", default=0)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def clean(self) -> None:
        if self.question.question_type == Question.TEXT:
            raise ValidationError(
                {"error": "Вопрос не может иметь предопределенных вариантов ответа"}
            )

        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save()


class UserPollResponse(models.Model):
    """
    Модель, в которой пользователь связан с опросом.
    """
    
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_poll_responses",
        verbose_name="Пользователь",
    )
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Опрос",
    )
    
    class Meta:
        verbose_name = "Данные об опросе, на который отвечает пользователь"
        verbose_name_plural = "Данные об опросах, на которые отвечает пользователь"


class UserQuestionResponse(models.Model):
    """
    Модель, в которой пользователь связан с вопросом.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_question_responses",
        verbose_name="Пользователь",
    )
    user_poll_response = models.ForeignKey(
        UserPollResponse,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Опрос пользователя",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Вопрос",
    )
    answer_text = models.TextField("Ответ в виде текста", null=True, blank=True)

    class Meta:
        verbose_name = "Данные о вопросе, на который отвечает пользователь"
        verbose_name_plural = "Данные о вопросах, на которые отвечает пользователь"

    def clean(self) -> None:
        if self.question.question_type != Question.TEXT and self.answer_text:
            raise ValidationError({"error": f"В вопросе с id {self.question.id} своим текстом запрещён"})

        user_answers_count = self.user.user_question_responses.filter(
            question=self.question
        ).count()

        if user_answers_count >= 1:
            raise ValidationError({"error": f"Вы уже отвечали на вопрос с id {self.question.id}"})

        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save()


class UserAnswer(models.Model):
    """
    Ответ пользователя.
    """

    user_question_response = models.ForeignKey(
        UserQuestionResponse,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Пользователь",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Ответ из предоставленных вариантов",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"

    def clean(self) -> None:
        if self.user_question_response.question.question_type == Question.TEXT:
            raise ValidationError(
                {"error": "У вопроса должен быть ответ своим текстом"}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save()
