import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers


def validate_year(year):
    """Проверка года."""
    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError(
            (f'Указанный год {year} больше текущего года {current_year}!'),
        )
    return year


def validate_username(username):
    """
    Пользовательский валидатор для имени пользователя.
    Проверяет, что имя пользователя
    не содержит недопустимых символов и не равно 'me'(USER_PATH).
    """
    if username == settings.USER_PATH:
        raise ValidationError(
            f'Имя пользователя не может быть { settings.USER_PATH}.'
        )
    # Регулярное выражение для допустимых символов
    regex = r'[\w.@+-]+'
    # Поиск недопустимых символов
    invalid_chars = re.sub(regex, '', username)
    if invalid_chars:
        invalid_chars_set = set(invalid_chars)
        invalid_chars_str = ''.join(invalid_chars_set)
        raise ValidationError(
            f'Недопустимые символы: {invalid_chars_str}.'
        )
    return username


def validate_signup_data(data):
    """Валидатор для данных регистрации."""
    username = data.get('username')
    email = data.get('email')
    exist_username = get_user_model().objects.filter(
            username=username
        ).first()
    exist_email = get_user_model().objects.filter(
            email=email
        ).first()
    if exist_username and not exist_email or (
        not exist_username and exist_email
    ):
        raise serializers.ValidationError(
            'username или email должны быть уникальны'
        )
    return data
