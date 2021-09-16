from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="polls-app.API",
        default_version='v1',
        description="Для авторизации необходимо получить токен в \
        эндпоинте /login, затем нажать на кнопку Authorize и подставить его следующим образом: Token tokenstring",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


urlpatterns = [
    path('swagger-ui/', schema_view.with_ui('swagger',
                                            cache_timeout=0), name='schema-swagger-ui')
]