from rest_framework import serializers
from books.models import Book
from user.models import User


class BookSerializer(serializers.ModelSerializer):
	"""Сериализатор для модели книг."""
	class Meta:
		model = Book
		fields = ('title', 'author', 'genre', 'reader')


class DebtorsSerializer(serializers.Serializer):
	"""Сриализатор информации для должников"""
	title = serializers.CharField()
	username = serializers.CharField()
	on_hands = serializers.DateTimeField()
	duration = serializers.DurationField()
