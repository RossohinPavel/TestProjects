from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import BadRequest

from books.models import Book
from .serializers import BookSerializer, DebtorsSerializer
from django.db.models import F, Max, ExpressionWrapper, fields, functions


# Create your views here.
class BookAPIViewSet(ViewSet):
	"""Вьюсет по книгам"""
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def list(self, request):
		"""Список всех книг в библиотеке"""
		queryset = Book.objects.all()
		serializer = BookSerializer(queryset, many=True)		
		return Response(serializer.data)

	@action(detail=False, methods=('GET', ))
	def debtors(self, request):
		"""Дополнительное действие для получения списка должников"""
		duration = ExpressionWrapper(
			functions.Now() - F('on_hands'), 
			output_field=fields.DurationField()
		)
		queryset = (
			Book.history.model.objects
			.exclude(reader_id=None)
			.values('title')
			.annotate(
				username=F('history_user_id__username'),
				on_hands=Max('history_date'),
				duration=duration
			)
		)
		serializer = DebtorsSerializer(queryset, many=True)	
		return Response(serializer.data)
	
	def retrieve(self, request, pk=None):
		"""Получение информации по 1 книге"""
		queryset = Book.objects.all()
		book = get_object_or_404(queryset, pk=pk)
		serializer = BookSerializer(book)
		return Response(serializer.data)

	def partial_update(self, request, pk=None):
		"""Через PATH запрос - получение и возврат книги"""
		queryset = Book.objects.all()
		book = get_object_or_404(queryset, pk=pk)
		if book.reader is not None and book.reader != request.user:
			raise BadRequest
		if book.reader is None:
			book.reader = request.user
		else:
			book.reader = None
		book.save()
		serializer = BookSerializer(book)
		return Response(serializer.data)
