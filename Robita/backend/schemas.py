"""Содержит pydantic-схемы"""
from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    """Pydantic представление пользователя"""
    telegram_id: int
    first_name: str
    last_name: str
    username: str
    birth_date: date
