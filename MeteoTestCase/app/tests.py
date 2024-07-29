from django.test import TestCase
from . service import forecast, statistics
from django.urls import reverse
from . models import City, Country


# Create your tests here.
class ForecastAPITestCase(TestCase):
	"""Проверка подключения к внешнему API"""

	def test_case_1(self):
		"""Получаем информцаию по городу"""
		params = {'name': 'Москва', 'count': 1, 'language': 'ru'}
		response = forecast.requests.get(forecast.CITY_SEARCH_URL, params=params)
		assert response.status_code == 200

	def test_case_2(self):
		"""Тестирование работы функции по получению информации о искомом городе"""
		city_loc = forecast._get_city_locations('Москва')
		# Нужные параметры для дальнейшего запроса
		params = ('country', 'name', 'latitude', 'longitude', 'timezone')
		for p in params:
			self.assertIn(p, city_loc)


	def test_case_3(self):
		"""Тестирование работы функции по получанию погоды"""
		city_loc = forecast._get_city_locations('Москва')
		raw_forecast = forecast._get_forecast(city_loc)
		# Нужные параметры для дальнейшего запроса
		self.assertIn('daily_units', raw_forecast)
		self.assertIn('daily', raw_forecast)
		# Функция ищет погоду по 4 дням: сегодня и на 3 дня вперед
		self.assertEqual(len(raw_forecast['daily']['time']), 4)


class AppTestCase(TestCase):
	"""Работа приложения"""
	PATH = reverse('home')

	def test_case_1(self):
		"""Гет запрос к основной странице"""
		response = self.client.get(self.PATH)
		self.assertEqual(response.status_code, 200)

	def test_case_2(self):
		"""Post запрос к основной странице с неправильным городом"""
		response = self.client.post(self.PATH, {'city': 'q'})
		self.assertEqual(response.status_code, 200)
		self.assertIn('error', response.context)

	def test_case_3(self):
		"""Post запрос к основной странице с нормальным городом"""
		response = self.client.post(self.PATH, {'city': 'Москва'})
		self.assertEqual(response.status_code, 200)
		self.assertIn('forecast', response.context)


class StatisticsTestCase(TestCase):
	"""Работа скрипта статистики"""
	PARAMS = {'country': 'Россия', 'city': 'Москва'}

	@classmethod
	def setUpTestData(cls):
		statistics.update_statistics(**cls.PARAMS)


	def test_case_1(self):
		"""Работа скрипта статистика"""
		country = Country.objects.filter(name=self.PARAMS['country']).first()
		self.assertTrue(country)
		self.assertEqual(country.querys, 1)
		city = City.objects.filter(name=self.PARAMS['city']).filter().first()
		self.assertTrue(city)
		self.assertEqual(city.querys, 1)

	def test_case_2(self):
		"""Обновим информацию для другово города"""
		city_name = 'Воронеж'
		params = self.PARAMS
		params['city'] = city_name
		statistics.update_statistics(**params)
		country = Country.objects.filter(name=params['country']).first()
		# для страны счетчик увеличился до 2х, так как оба тестовых города находятся в 1 стране
		self.assertTrue(country)
		self.assertEqual(country.querys, 2)
