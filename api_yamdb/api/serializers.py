from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.constans import (
    NAME_LENGTH,
    MIN_SCORE,
    MAX_SCORE,
    NAME_LENGTH,
    EMAIL_LENGTH
)
from reviews.models import Categorie, Comment, Genre, Title, Review, User
from reviews.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categorie."""

    class Meta:
        model = Categorie
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')


class ReadTitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title с дополнительным полем 'rating'.
    Используется для чтения данных.
    """
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    def validate_username(self, username):
        return validate_username(username)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(
        max_length=NAME_LENGTH,
        required=True,
        validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
        required=True,
    )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена"""
    username = serializers.CharField(
        required=True,
        max_length=NAME_LENGTH,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CONFIRMATION_CODE_LENGTH
    )

    def validate(self, data):
        """
        Валидация, проверяющая, что пользователь существует,
        и код подтверждения корректный.
        """
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            user.confirmation_code = settings.INVALID_CONFIRMATION_CODE
            user.save()
            raise serializers.ValidationError(
                "Код подтверждения неверен."
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        min_value=MIN_SCORE,
        max_value=MAX_SCORE
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        """Проверка отзыва."""
        request = self.context['request']
        if request.method == "PATCH":
            return data
        visitor = request.user
        title = (
            request.parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=visitor, title=title):
            raise serializers.ValidationError(
                'Пользователь может оставлять только один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
