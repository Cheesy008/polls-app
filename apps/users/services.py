from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


def login_user(*, username: str, password: str) -> tuple[str, User]:
    """
    Авторизация пользователя.

    Если предоставленные данные валидны, то генерирурем токен
    и возвращаем его.
    """
    user = authenticate(username=username, password=password)
    if not user:
        raise ValidationError("Неверные данные пользователя")

    token, _ = Token.objects.get_or_create(user=user)

    return token.key, user


def create_anonymous_user() -> User:
    """
    Создаёт анонимного пользователя.
    
    Ник генерируется на основе последнего id из бд.
    """
    last_id = User.objects.last().id
    return User.objects.create_user(username=f"anon_user_{last_id}")
