from rest_framework import serializers

from reviews.models import Categorie, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
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
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Юзера"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для создания учетки"""
    pass


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена"""
    pass


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ['role'] 