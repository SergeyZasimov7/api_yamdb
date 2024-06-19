from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy

from .validators import validate_year


class User(AbstractUser):
    """Модель класса User унаследованная от AbstractUser"""

    class Role(models.TextChoices):
        USER = 'user', gettext_lazy('Пользователь')
        MODERATOR = 'moderator', gettext_lazy('Модератор')
        ADMIN = 'admin', gettext_lazy('Администратор')
        SUPERUSER = 'superuser', gettext_lazy('Суперюзер')

    username = models.CharField(
        max_length=150,
        verbose_name='Имя',
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=40,
        verbose_name='Роль',
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR


class Categorie(models.Model):
    """Модель для категорий."""
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений."""
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='год выпуска',
        validators=[
            validate_year
        ]
    )
    description = models.TextField(
        verbose_name='описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
    )
    category = models.ForeignKey(
        Categorie,
        verbose_name='категория',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
