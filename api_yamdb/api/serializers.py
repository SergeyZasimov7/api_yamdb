from rest_framework import serializers

from reviews.models import Categorie, Genre, Title, User


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


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title с дополнительным полем 'rating'.
    Используется для чтения данных.
    """
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена"""
    pass


class UserMeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User,
    используемый для редактирования данных текущего пользователя.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ['role']
