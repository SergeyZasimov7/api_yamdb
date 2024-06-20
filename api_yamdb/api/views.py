import random
import string
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAdminOrSuperuser
)
from reviews.models import Categorie, Genre, Title, User
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    UserSerializer,
    ReadOnlyTitleSerializer,
    UserMeSerializer,
    TokenSerializer
)
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet


class TokenObtainPairView(TokenObtainPairView):
    """View для получения токена."""
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        """Метод обработки POST запроса."""
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not username or not confirmation_code:
            return Response(
                {'error': 'Username and confirmation code are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.confirmation_code != confirmation_code:
            return Response(
                {'error': 'Invalid confirmation code.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = self.get_token(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )

    def get_token(self, user):
        """Метод для обновления токена."""
        refresh = RefreshToken.for_user(user)
        return refresh


def generate_confirmation_code(length=6):
    """Генерация кода подтверждения заданной длины."""
    return ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=length
    ))


class UserRegistrationView(APIView):
    """View для регистрации нового пользователя."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Регистрирует нового пользователя."""
        username = request.data.get('username')
        email = request.data.get('email')
        if username == 'me':
            return Response(
                {'error': 'Username "me" is not allowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            if existing_user.email == email:
                confirmation_code = generate_confirmation_code()
                existing_user.confirmation_code = confirmation_code
                existing_user.save()
                self.send_confirmation_email(
                    existing_user.email,
                    confirmation_code
                )
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
            if User.objects.filter(email=email).exists():
                return Response(
                    {'email': 'Пользователь с таким email уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                confirmation_code = generate_confirmation_code()
                user = serializer.save(confirmation_code=confirmation_code)
                self.send_confirmation_email(user.email, confirmation_code)
                return Response(
                    {'username': user.username, 'email': user.email},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

    def send_confirmation_email(self, email, confirmation_code):
        """Отправляет email с кодом подтверждения."""
        subject = 'Код подтверждения регистрации'
        message = f'Ваш код подтверждения: {confirmation_code}'
        from_email = 'email@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


class UserMeView(RetrieveUpdateAPIView):
    """View для получения и обновления информации о текущем пользователе."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_object(self):
        """Получение объекта пользователя."""
        return self.request.user

class UserByUsernameView(RetrieveAPIView, DestroyModelMixin):
    """
    View для получения,
    обновления и удаления информации о пользователе по имени.
    """
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    
    def get(self, request, *args, **kwargs):
        """Получение информации о пользователе."""
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """Удаление информации о пользователе."""
        return self.destroy(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Удаление объекта пользователя."""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, *args, **kwargs):
        """Частичное обновление информации о пользователе."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    """View для получения списка всех пользователей."""
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def post(self, request):
        """Создает нового пользователя."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Метод для работы с текущим пользователем."""
        if request.method == 'PATCH':
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
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet для категорий."""
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


# class TitleViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all().order_by('name')
#     permission_classes = (IsAdminOrReadOnly,)
#     serializer_class = TitleSerializer
#     filterset_class = TitleFilter
#     filter_backends = [DjangoFilterBackend]
#     http_method_names = ['get', 'post', 'patch', 'delete']
#     def get_serializer_class(self):
#         if self.action in ('retrieve', 'list'):
#             return ReadOnlyTitleSerializer
#         return TitleSerializer
from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def put_method_not_allowed(view_func):
    """Декоратор запрета PUT запроса."""
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        """Функция проверки запроса."""
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all().order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_serializer_class(self):
        """Метод определения класса сериализатора."""
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer
    
    @put_method_not_allowed
    def update(self, request, *args, **kwargs):
        """Метод обновления записи о произведении."""
        return super().update(request, *args, **kwargs)