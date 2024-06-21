from rest_framework import serializers

from reviews.models import Categorie, Comment, Genre, Title, Review, User


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
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """
        Валидация, проверяющая, что пользователь существует,
        и код подтверждения корректный.
        """
        username = data['username']
        confirmation_code = data['confirmation_code']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким именем не найден."
            )

        if not user.confirmation_code == confirmation_code:
            raise serializers.ValidationError(
                "Код подтверждения неверен."
            )

        return data


class UserMeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User,
    используемый для редактирования данных текущего пользователя.
    """
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ['role']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('author', 'title')

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                'Оценка выставляется от 1 до 10!'
            )
        return value

    def validate(self, request):
        if self.context['request'].method != "PATCH":
            author = self.context['request'].user
            title = self.context['request'].parser_context['kwargs']['title_id']
            if Review.objects.filter(author=author, title=title):
                raise serializers.ValidationError(
                    'Пользователь может оставлять только один отзыв!')
        return request


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'review')