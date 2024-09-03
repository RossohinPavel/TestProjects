from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	"""Расширение модели пользователя"""

	# Для пользователя
	address = models.CharField(max_length=255)

	# Для сотрудника
	personnel_number = models.PositiveIntegerField(null=True)
