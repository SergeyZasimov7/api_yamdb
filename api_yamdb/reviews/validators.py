import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


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
        invalid_chars_str = ', '.join(invalid_chars_set)
        invalid_count = len(invalid_chars)
        raise ValidationError(
            f'Недопустимые символы в имени пользователя: {invalid_chars_str}.'
            f'Количество недопустимых символов: {invalid_count}.'
        )
    return username
