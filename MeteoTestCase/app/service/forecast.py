"""Утилиты для работы с запросами к погодному сайту"""
import requests
import json
from django.utils import timezone
from datetime import timedelta
from . import statistics


CITY_SEARCH_URL = 'https://geocoding-api.open-meteo.com/v1/search'
FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'

# Параметры для daily: Минимальная и максимальная температукра, вероятность осадков, скорость ветра
DAILY_PARAMS = 'temperature_2m_min,temperature_2m_max,precipitation_probability_max,wind_speed_10m_max'


class UserException(Exception):
    pass


def get_forecast(city_name: str):
    """Основная функция для получения погоды."""
    try:
        city_loc = _get_city_locations(city_name)
        raw_forecast = _get_forecast(city_loc)
        forecast = _format_forecast(city_loc, raw_forecast)
        statistics.update_statistics(forecast['country'], forecast['city'])
        return forecast
    except UserException as ue:
        return(str(ue))


def _get_city_locations(city_name: str) -> dict:
    """Возвращает координаты города"""
    params = {'name': city_name, 'count': 1, 'language': 'ru'}
    response = requests.get(CITY_SEARCH_URL, params=params)
    results = json.loads(response.content)
    if 'results' not in results:
        raise UserException(f'Похоже, что города {city_name} нет в списке городов.')
    return results['results'][0]


def _get_forecast(city_loc: dict):
    """Собсна, получаем погоду"""
    # Парамертры для запроса 
    start_date = timezone.now().date()
    end_date = (start_date + timedelta(days=3)) # На 3 дня вперед
    params = {
        'latitude': city_loc['latitude'],       # Широта
        'longitude': city_loc['longitude'],     # Долгота
        'timezone': city_loc['timezone'],       # Зона времени
        'time_mode': 'time_interval',           # По временным интервалам - дням
        'start_date': start_date,               # От 
        'end_date': end_date,                 # До
        'daily': DAILY_PARAMS                   # Типы погодной информации, которую будем получать
    }
    r = requests.get(FORECAST_URL, params=params)
    results = json.loads(r.content)
    return results


def _format_forecast(city_loc: dict, raw_forecast: dict) -> dict:
    """форматируем погоду"""
    data = {
        'country': city_loc['country'],
        'city': city_loc['name'],
        'daily_units': raw_forecast['daily_units'],
        'daily': raw_forecast['daily']
    }
    return data
