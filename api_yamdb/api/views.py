import random

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly
)

from reviews.models import Categorie, Genre, Title, Review, User
from reviews.constans import ALLOWED_REQUESTS
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    TitleSerializer,
    TokenSerializer,
    ReadTitleSerializer,
    ReviewSerializer,
    UserSerializer
)
from .filters import TitleFilter


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request):
    """Функция для получения токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.get(username=serializer.validated_data.get('username'))
    return Response({
        'token': str(RefreshToken.for_user(user).access_token)
    }, status=status.HTTP_200_OK)


def generate_confirmation_code():
    """Генерация кода подтверждения заданной длины."""
    return ''.join(random.choices(
        settings.CONFIRMATION_CODE_ALLOWED_CHARS,
        k=settings.CONFIRMATION_CODE_LENGTH
    ))


class UserRegistrationView(APIView):
    """View для регистрации нового пользователя."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Регистрирует нового пользователя."""
        username = request.data.get('username')
        email = request.data.get('email')
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            if existing_user.email == email:
                return Response(
                    {
                        'username': existing_user.username,
                        'email': existing_user.email
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'email': 'Пользователь с таким email уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            confirmation_code = generate_confirmation_code()
            user = serializer.save(confirmation_code=confirmation_code)
            self.send_confirmation_email(user.email, confirmation_code)
            return Response(
                {'username': user.username, 'email': user.email},
                status=status.HTTP_200_OK
            )

    def send_confirmation_email(self, email, confirmation_code):
        """Отправляет email с кодом подтверждения."""
        subject = 'Код подтверждения регистрации'
        message = f'Ваш код подтверждения: {confirmation_code}'
        from_email = settings.USER_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path=settings.USER_PATH,
        url_name=settings.USER_PATH,
        permission_classes=(IsAuthenticated,)
    )
    def current_user(self, request):
        """Метод для работы с текущим пользователем."""
        if request.method != 'PATCH':
            return Response(
                self.get_serializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            role=request.user.role,
            partial=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseCategoryGenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Базовый набор миксинов, который предоставляет действия:
    "перечислить", "создать" и "удалить".
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(BaseCategoryGenreViewSet):
    """ViewSet для категорий."""
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend]
    http_method_names = ALLOWED_REQUESTS

    def get_serializer_class(self):
        """Метод определения класса сериализатора."""
        if self.action in ('retrieve', 'list'):
            return ReadTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает API запросы к моделе Review."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ALLOWED_REQUESTS

    def get_post(self):
        """Возвращает объект Title c id из запроса."""
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        """Переопределение функции возврата списка отзывов."""
        return self.get_post().reviews.all()

    def perform_create(self, serializer):
        """Переопределение функции создания отзыва."""
        serializer.save(
            author=self.request.user,
            title=self.get_post())


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает API запросы к моделе Comment."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ALLOWED_REQUESTS

    def get_post(self):
        """Возвращает объект Post c id из запроса."""
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        """Переопределение функции возврата списка комментариев."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Переопределение функции создания комментария."""
        serializer.save(
            author=self.request.user,
            review=self.get_post())
