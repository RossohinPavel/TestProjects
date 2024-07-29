from django.db import models

# Create your models here.
class City(models.Model):
	"""Города и счетчики для них"""
	name = models.CharField(max_length=255, unique=True)
	querys = models.PositiveIntegerField(default=0)
	country = models.ForeignKey(to='Country', on_delete=models.CASCADE, related_name='citys')


class Country(models.Model):
	"""Страны и счетчики для них"""
	name = models.CharField(max_length=255, unique=True)
	querys = models.PositiveIntegerField(default=0)
