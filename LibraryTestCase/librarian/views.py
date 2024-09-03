from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import Book
from datetime import timedelta


class DebtorsView(LoginRequiredMixin, ListView):
	"""Вьюха для отображения должников для сотрудников библиотеки"""
	template_name = 'librarian/debtors.html'
	extra_context = {
		'title': 'Список должников',
		'links': {'Список должников': 'home'}
	}
	paginate_by = 5

	def get_queryset(self):
		"""Формирует выборку по должникам"""
		books = Book.objects.raw(
			"""
			SELECT 
				id, 
				reader_id,
				title, 
				author,
				date(MAX(history_date), 'localtime') as history_date,
				unixepoch('now') - unixepoch(MAX(history_date)) as duration
			FROM books_historicalbook
			GROUP BY title
			HAVING reader_id IS NOT NULL
			"""
		)
		for book in books:
			book.duration = timedelta(seconds=book.duration).days
		return books