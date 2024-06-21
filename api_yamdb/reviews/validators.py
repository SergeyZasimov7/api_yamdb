import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    """Проверка года."""
    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError(
            (f'Указанный год {year} больше текущего года {current_year}!'),
        )


def validate_username(value):
    """
    Пользовательский валидатор для имени пользователя.
    Проверяет, что имя пользователя
    не содержит недопустимых символов и не равно 'me'.
    """
    if value == 'me':
        raise ValidationError('Имя пользователя не может быть "me".')

    # Регулярное выражение для допустимых символов
    regex = r'^[\w.@+-]+\Z'
    if not re.match(regex, value):
        # Найти все недопустимые символы
        invalid_chars = set(re.sub(regex, '', value))
        invalid_chars_str = ', '.join(sorted(invalid_chars))
        raise ValidationError(
            f'Недопустимые символы в имени пользователя: {invalid_chars_str}.'
        )
