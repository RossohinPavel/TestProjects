from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import getenv


class SQLite:
    """Конфиг для настройки sqlite-базы данных"""

    def __init__(self):
        self.url = 'sqlite:///db.sqlite3'
        self.engine = None

    def create_session(self):
        """Создает сессию"""
        from sqlalchemy import create_engine
        self.engine = create_engine(self.url)
        return sessionmaker(self.engine, expire_on_commit=False)


class Postgres:
    """Настройки Postgres"""
    HOST: str = str(getenv("POSTGRES_HOST", ""))
    PORT: str = str(getenv("POSTGRES_PORT", ""))
    USER: str = str(getenv("POSTGRES_USER", ""))
    PASS: str = str(getenv("POSTGRES_PASSWORD", ""))
    NAME: str = str(getenv("POSTGRES_NAME", ""))

    def __init__(self):
        self.engine = None

    @property
    def async_url(self) -> str:
        return f'asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'

    url = async_url

    def create_async_session(self):
        """Создает асинхронную сессию под Postgress"""
        self.engine = create_async_engine(self.async_url)
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    create_session = create_async_session


BASE = SQLite()
BaseSession = BASE.create_session()
