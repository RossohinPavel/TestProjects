from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F, Value
from .models import Book
from datetime import timedelta


class BookMixin:
	"""Миксин с общей для пользователей библиотеки логикой"""
	template_name = 'books/list.html'
	book_objects = Book.objects.all()

	def post(self, request):
		"""обработка запроса для получения книги"""
		book = Book.objects.get(pk=request.POST['book_id'])
		self.__read(book, request)
		book.save()
		return self.get(request)

	@staticmethod
	def __read(book, request):
		"""Устанавливает или снимает читателя"""
		if book.reader is None:
			book.reader = request.user
			return
		if book.reader == request.user:
			book.reader = None
			return
	
	def get_context_data(self, **kwargs):
		"""Формирование общего контекста для странички"""
		context: dict = super().get_context_data(**kwargs)
		context['links'] = {"Список Книг": "home", "Мои книги": "mybooks"}
		context['paginator'] = Paginator(kwargs['books'], 5)
		page_number = self.request.GET.get('page')
		context['page_obj'] = context['paginator'].get_page(page_number)
		return context


# Create your views here.
class BooksList(BookMixin, LoginRequiredMixin, TemplateView):
	"""Вьюха для отображения списка книг"""
	extra_context = {'title': 'Список книг'}

	def get_context_data(self, **kwargs):
		"""Отображение списка книг. Исключает книги взятые пользователем"""
		kwargs['books'] = self.book_objects.exclude(reader=self.request.user)
		return super().get_context_data(**kwargs)


class MyBooks(BookMixin, LoginRequiredMixin, TemplateView):
	"""Вьюха для отображения списка Моих книг"""
	extra_context = {'title': 'Мои книги'}

	def get_context_data(self, **kwargs):
		"""Формирует выборку из книг, которые находятся на руках у текущего пользователя"""
		books = self.book_objects.raw(
			"""
			SELECT 
				id, 
				title, 
				date(MAX(history_date), 'localtime') as history_date,
				unixepoch('now') - unixepoch(MAX(history_date)) as duration,
				reader_id
			FROM books_historicalbook
			GROUP BY title
			HAVING reader_id = %s
			""",
			[self.request.user.id]
		)
		for book in books:
			book.duration = timedelta(seconds=book.duration).days
		kwargs['books'] = books
		return super().get_context_data(**kwargs)
