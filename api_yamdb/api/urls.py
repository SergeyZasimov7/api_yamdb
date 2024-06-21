from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    TitleViewSet,
    SlidingTokenObtainView,
    ReviewViewSet,
    UserRegistrationView,
    UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='title-reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='review-comments'
)
auth_urls = [
    path('v1/auth/token/', SlidingTokenObtainView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', UserRegistrationView.as_view(), name='signup'),
]

urlpatterns = [
    *auth_urls,
    path('v1/', include(router_v1.urls)),
]
