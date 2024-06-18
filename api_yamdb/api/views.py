from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .permissions import IsAdminOrReadOnly
from .models import Categorie, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReadOnlyTitleSerializer,)

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer
