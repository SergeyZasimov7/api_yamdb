from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year, validate_username
from .constans import NAME_LENGTH, MIN_SCORE, MAX_SCORE, SLICE_NAME_OBJECT


class User(AbstractUser):
    """Модель класса User унаследованная от AbstractUser"""

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
    confirmation_code = models.CharField(max_length=6, blank=True)
    email = models.EmailField(
        max_length=254,
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
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR


class BaseCategoryGenre(models.Model):
    """Базовый класс для категорий и жанров."""
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
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Categorie(BaseCategoryGenre):
    """Модель для категорий."""
    pass


class Genre(BaseCategoryGenre):
    """Модель для жанров."""
    pass


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
        ordering = ['name']

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    """Базовый класс для моделей отзывов и комментариев."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('text',)


class Review(BaseModel):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:SLICE_NAME_OBJECT]


class Comment(BaseModel):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
