"""Скрипты для обновления статистики"""
from app import models
from django.db.models import F


def update_statistics(country: str, city: str):
	"""Обновление статистики по городу."""
	_city = _get_city_record(country, city)
	_city.country.querys = F('querys') + 1
	_city.country.save()
	_city.querys = F('querys') + 1
	_city.save()


def _get_country_record(country: str) -> models.Country:
	"""Получение объекта страны. При необходимости его создание."""
	_country = models.Country.objects.filter(name=country).first()
	if _country is None:
		_country = models.Country(name=country)
		_country.save()
	return _country


def _get_city_record(country: str, city: str) -> models.City:
	"""Получение объекта города. При необходимости его создание."""
	_city = models.City.objects.filter(country__name=country, name=city).first()
	if _city is None:
		_country = _get_country_record(country)
		_city = models.City(country=_country, name=city)
		_city.save()
	return _city
