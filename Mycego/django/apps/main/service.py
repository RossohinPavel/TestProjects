"""
Скрипт с набором функций для отправки запросов.

Поиграться с составлением REST API запросов яндекса можно здесь
https://yandex.ru/dev/disk/poligon/
"""
import requests
from urllib.parse import urlencode

from functools import wraps
from django.core.cache import cache


BASE_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
DOWNLOAD_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'


def cache_decorator(func):
	"""Декоратор для низкоуровневого кширования функций запроса"""
	@wraps(func)
	def wrapper(url: str) -> dict:
		res = cache.get(url, None)
		if res:
			return res
		res = func(url)
		cache.set(url, res, 300)
		return res
	return wrapper


@cache_decorator
def get_file_data(url: str) -> dict:
	"""Формирует словарь для представления файлов"""
	main_response = make_request(BASE_URL, public_key=url, limit=50_000)
	parse_items(main_response)
	download_all_link = make_request(DOWNLOAD_URL, public_key=url, field='href')['href']
	data = {
		'name': main_response['name'],
		'public_url': url,
		'download_all': download_all_link,
		'items': main_response['_embedded']['items'],
		'filters': main_response['filters']
	}
	return data


def make_request(base: str, **params) -> dict:
	"""Делает запрос к апи и возвращает разпарсеный словарь json"""
	request = urlencode(params)
	final_url = base + request
	res = requests.get(final_url)
	return res.json()


def parse_items(data: dict):
	"""Добавляет для папок атрибуты, как на файлах. Формирует фильтры"""
	data['filters'] = set()
	for item in data['_embedded']['items']:
		if item['type'] == 'dir':
			item['media_type'] = 'dir'
			if 'public_url' in item:
				item['file'] = make_request(
					DOWNLOAD_URL, 
					public_key=item['public_url'],
					field='href'
				)['href']
		data['filters'].add(item['media_type'])
