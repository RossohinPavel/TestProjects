from django.shortcuts import render
from books.views import BooksList
from librarian.views import DebtorsView
from django.core.handlers.wsgi import WSGIRequest


# Create your views here.
def index(request: WSGIRequest):
	"""Логика работы главной страницы. Перенаправляет на страницы в зависимости от статуса пользователя"""
	if not request.user.is_authenticated:
		return render(request, 'nav.html', context={'title': 'Библиотека'})

	if request.user.is_staff:
		return DebtorsView.as_view()(request)

	return BooksList.as_view()(request)
