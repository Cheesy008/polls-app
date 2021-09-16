from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

from .serializers import PollListSerializer, PollSerializer, SendUserAnswerSerializer
from .models import Poll
from .permissions import IsPollOwnerOrReadOnly, IsAdminUserOrReadOnly
from utils.api_errors_mixin import ApiErrorsMixin
from apps.polls.services import create_vote


class PollsViewSet(ApiErrorsMixin, viewsets.ModelViewSet):
    list_serializer_class = PollListSerializer
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    permission_classes = (
        IsAdminUserOrReadOnly,
        IsPollOwnerOrReadOnly,
    )
    http_method_names = ("get", "post", "list", "put", "delete")

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.serializer_class

    def get_queryset(self):
        # если пользователь не является админом, то выводим только активные опросы
        if self.request.user.is_superuser:
            return Poll.objects.all()
        return Poll.objects.active_polls()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # удаление поля start_date, т.к. его нельзя редактировать
        serializer.validated_data.pop("start_date", None)
        serializer.save()

    @swagger_auto_schema(
        method="post", request_body=SendUserAnswerSerializer(many=True)
    )
    @action(
        detail=True, methods=["post"], url_path="vote", permission_classes=(AllowAny,)
    )
    def vote(self, request, pk, *args, **kwargs):
        """
        Эндпоинт для голосования.
        
        Необходимо передать id вопроса, массив с id ответов
        или текст ответа, в зависимости от типа вопроса.
        """
        serializer = SendUserAnswerSerializer(
            data=request.data,
            many=True,
            context={"poll_id": pk},
        )
        serializer.is_valid(raise_exception=True)
        create_vote(data=serializer.validated_data, user=request.user, poll_id=pk)

        return Response(
            {"message": "Вы успешно ответили на вопрос"},
            status=status.HTTP_200_OK,
        )
