from django.urls import path
from . import views

urlpatterns = [
    path('mybooks/', views.MyBooks.as_view(), name='mybooks'),
]