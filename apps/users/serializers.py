from rest_framework import serializers
from django.contrib.auth import get_user_model

from .services import login_user
from apps.polls.models import UserPollResponse, UserQuestionResponse, UserAnswer
from apps.polls.serializers import AnswerSerializer, QuestionSerializer


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    Сериалайзер для авторизации пользователя.
    """

    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        required=True,
        write_only=True,
        help_text="Пароль",
    )

    def create(self, validated_data):
        token, user = login_user(**validated_data)
        return token, user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода данных о пользователе.
    """

    class Meta:
        model = User
        fields = ("id", "username")
        read_only_fields = ("__all__",)


class AuthOutputSerializer(serializers.Serializer):
    """
    Сериалайзер для вывода токена и пользователя.
    """

    token = serializers.CharField(read_only=True, help_text="Токен для авторизации")
    user = UserSerializer(read_only=True, help_text="Модель пользователя")


# region polls_stats


class UserAnswerSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()
    
    class Meta:
        model = UserAnswer
        fields = ("id", "answer")
        read_only_fields = ("__all__",)


class UserQuestionResponseSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source="question.question_text")
    question_type = serializers.CharField(source="question.question_type")
    answers = UserAnswerSerializer(many=True)

    class Meta:
        model = UserQuestionResponse
        fields = ("id", "question_text", "question_type", "answers", "answer_text")
        read_only_fields = ("__all__",)


class UserPollResponseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="poll.title")
    questions = UserQuestionResponseSerializer(many=True)

    class Meta:
        model = UserPollResponse
        fields = ("id", "title", "questions")
        read_only_fields = ("__all__",)


class UserPollsStatsSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода данных о прохождении опросов.
    """
    user_poll_responses = UserPollResponseSerializer(many=True)
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "user_poll_responses",
        )
        read_only_fields = ("__all__",)


# endregion
