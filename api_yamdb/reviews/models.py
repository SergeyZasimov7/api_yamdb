from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year, validate_username
from .constans import (
    NAME_LENGTH,
    MIN_SCORE,
    MAX_SCORE,
    SLICE_NAME_OBJECT,
    EMAIL_LENGTH
)


class User(AbstractUser):
    """Модель для пользователя."""

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Имя',
        unique=True,
        validators=[validate_username]
    )
    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        blank=True
    )
    confirmation_attempts = models.IntegerField(default=0)
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        verbose_name='Почта',
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=max(len(role) for role, _ in Role.choices),
        verbose_name='Роль',
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    def get_confirmation_attempts(self):
        return self.confirmation_attempts


class BaseNamedSlugModel(models.Model):
    """Базовый модель, содержащая поля 'name' и 'slug'."""
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='метка',
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Categorie(BaseNamedSlugModel):
    """Модель для категорий."""

    class Meta(BaseNamedSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseNamedSlugModel):
    """Модель для жанров."""

    class Meta(BaseNamedSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


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
        related_name='titles'
    )
    category = models.ForeignKey(
        Categorie,
        verbose_name='категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseTextDateAuthorModel(models.Model):
    """Базовый класс для моделей отзывов и комментариев."""
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:SLICE_NAME_OBJECT]


class Review(BaseTextDateAuthorModel):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ], verbose_name='Оценка'
    )

    class Meta(BaseTextDateAuthorModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]


class Comment(BaseTextDateAuthorModel):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(BaseTextDateAuthorModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
