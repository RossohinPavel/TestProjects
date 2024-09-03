from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.parser.models import Log
from apps.api.v1.serializers import LogSerializer


class LogPagination(PageNumberPagination):
    """Настройки пагинации"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class LogViewSet(viewsets.ModelViewSet):
    """Представление для лога"""
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    pagination_class = LogPagination
    http_method_names = ("get", "head", "options")

    # Фильтры
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('ip', 'method')
    filterset_fields = ('date',  'uri', 'status_code')