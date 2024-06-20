from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    TokenObtainPairView,
    UserViewSet,
    UserRegistrationView,
    UserMeView,
    UserByUsernameView
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

router_v1.register(
    'categories',
    CategoryViewSet
)
router_v1.register(
    'genres',
    GenreViewSet
)
router_v1.register(
    'titles',
    TitleViewSet
)

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('v1/users/me/', UserMeView.as_view(), name='user_me'),
    path('v1/users/<str:username>/', UserByUsernameView.as_view(),
         name='user_by_username'),
    path('v1/', include(router_v1.urls)),
]
