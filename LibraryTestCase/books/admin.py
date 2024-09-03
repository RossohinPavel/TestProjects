from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Book
from user.models import User

# Register your models here.

@admin.register(Book.history.model)
class BookHistory(SimpleHistoryAdmin):
	"""Отображение истории взятия книг в адмике"""
	list_display = ('history_id', 'reader', 'title', 'author', 'genre')
	list_display_links = ('history_id', )
	list_per_page = 20
	# Фильтр по истории читателей
	list_filter = ('reader', )


class BooksFilter(admin.SimpleListFilter):
	"""Фильтр для админки отображения книг, которые находятся на руках"""
	title = 'Книги на Руках'
	parameter_name = 'reader'
    
	def lookups(self, request, model_admin):
		users = User.objects.values('id', 'username')
		lst = [('__all__', 'Все книги на руках')]
		lst.extend((u['id'], u['username']) for u in users)
		return lst

	def queryset(self, request, queryset):
		reader = self.value()
		if reader is None:
			return queryset
		if reader == '__all__':
			return queryset.exclude(reader=None)
		return queryset.filter(reader=reader)


@admin.register(Book)
class BookAdmin(SimpleHistoryAdmin):
	"""Пердставление для модели книг"""
	list_display = ('id', 'title', 'author', 'genre', 'reader')
	list_display_links = ('id', 'title')
	ordering = ('id', )
	list_per_page = 20
	# Фильтр по актуальным читателям
	list_filter = (BooksFilter, )