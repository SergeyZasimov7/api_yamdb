from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_year, validate_username
from .constans import name_length


class User(AbstractUser):
    """Модель класса User унаследованная от AbstractUser"""

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(
        max_length=name_length,
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


class Review(models.Model):
    """Модель отзывов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
