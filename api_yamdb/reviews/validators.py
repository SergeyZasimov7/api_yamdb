from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка года."""
    if value > timezone.now().year:
        raise ValidationError(
            ('Указанный год больше текущего!'),
            params={'value': value},
        )
