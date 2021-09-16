from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    LoginSerializer,
    AuthOutputSerializer,
    UserPollsStatsSerializer,
)


User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(method="post", request_body=LoginSerializer())
    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        return Response(
            AuthOutputSerializer({"token": token, "user": user}).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def logout(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="user-stats",
    )
    def get_user_stats(self, request, pk, *args, **kwargs):
        """
        Получение статистики по опросам конкретного пользователя.
        """
        user = get_object_or_404(User, id=pk)
        return Response(
            UserPollsStatsSerializer(user).data,
            status.HTTP_200_OK,
        )
