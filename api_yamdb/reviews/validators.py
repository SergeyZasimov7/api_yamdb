import re

from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.settings import USER_PATH


def validate_year(year):
    """Проверка года."""
    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError(
            (f'Указанный год {year} больше текущего года {current_year}!'),
        )
    return year


def validate_username(named):
    """
    Пользовательский валидатор для имени пользователя.
    Проверяет, что имя пользователя
    не содержит недопустимых символов и не равно 'me'(USER_PATH).
    """
    USER_PATH = 'me'
    if named == USER_PATH:
        raise ValidationError('Имя пользователя не может быть "me".')
    # Регулярное выражение для допустимых символов
    regex = r'[\w.@+-]+'
    # Поиск недопустимых символов
    invalid_chars = set(re.sub(regex, '', named))
    if invalid_chars:
        invalid_chars_str = ', '.join(invalid_chars)
        raise ValidationError(
            f'Недопустимые символы в имени пользователя: {invalid_chars_str}.'
        )
    return named
