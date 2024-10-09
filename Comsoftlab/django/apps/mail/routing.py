"""
Скрипт обработки маршрутов channels части приложения
"""

from django.urls import path
from .consumers import WSConsumer


ws_urlpatterns = [
    path('ws/mail/', WSConsumer.as_asgi())
]
