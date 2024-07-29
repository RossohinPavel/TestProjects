from rest_framework.test import APITestCase
from app import models
from app.service import statistics


# Create your tests here.
class StatisticsTestCase(APITestCase):
	"""Тестирование API"""

	@classmethod
	def setUpTestData(cls):
		# Set up data for the whole TestCase
		statistics.update_statistics('Россия', 'Москва')
		statistics.update_statistics('Россия', 'Москва')
		statistics.update_statistics('Россия', 'Воронеж')
		statistics.update_statistics('США', 'Вашингтон')

	def test_case_1(self):
		"""С параметром запроса city. Должен выдать информацию по городу"""
		city = 'Москва'
		response = self.client.get('/api/', {'city': city})
		self.assertIn('name', response.data)
		self.assertEqual(response.data['name'], city)
		self.assertIn('country', response.data)
		self.assertEqual(response.data['country'], 'Россия')
		self.assertIn('querys', response.data)
		self.assertEqual(response.data['querys'], 2)

	def test_case_2(self):
		"""C парамтером запроса country. Должен выдать информацию по стране и всем городам"""
		country = 'Россия'
		response = self.client.get('/api/', {'country': country})
		self.assertIn('name', response.data)
		self.assertEqual(response.data['name'], country)
		self.assertIn('querys', response.data)
		self.assertEqual(response.data['querys'], 3) # 2 обращения к Москве и 1 к Воронежу
		self.assertIn('citys', response.data)
		self.assertEqual(len(response.data['citys']), 2)

	def test_case_3(self):
		"""Тест ответа без параметров"""
		# выдает список того, что было проверено в предыдущих методах
		response = self.client.get('/api/')
		self.assertEqual(len(response.data), 2)


# 	def test_case_1(self):
# 		"""Тест для получения информации по городу"""
# 		response = self.client.get('/api')
# 		print(response.data)