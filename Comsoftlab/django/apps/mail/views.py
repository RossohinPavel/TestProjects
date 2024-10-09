from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from .models import Mail


class MailView(ListView):
    """Представление для писем"""
    paginate_by = 10
    template_name = 'index.html'
    context_object_name = 'mails'

    def get_queryset(self) -> QuerySet[Any]:
        """Выборка всех писем с пагинацией и с сортировкой по id по убыванию."""
        return Mail.objects.all().order_by('-id')
