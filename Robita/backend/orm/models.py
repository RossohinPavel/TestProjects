"""Скрипт с описанием модели и orm-командами"""
from tortoise import Tortoise, fields, models


class User(models.Model):
	"""Представление пользователя в БД"""
	telegram_id = fields.IntField(primary_key=True, db_index=True)
	first_name = fields.CharField(max_length=50)
	last_name = fields.CharField(max_length=50)
	username = fields.CharField(max_length=50)
	birth_date = fields.DatetimeField()

	class Meta:
		table = 'user'

	def __str__(self):
		return self.username
