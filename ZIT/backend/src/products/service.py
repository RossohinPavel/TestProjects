from sqlalchemy import select
from functools import wraps

from src.datebase import BaseSession, AsyncSession
from . import models
from . import schemas


def session_decorator_async(func):
    """Декоратор для выдачи сессий на функции"""
    @wraps(func)
    async def inner(*args, **kwargs):
        async with BaseSession() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                print(e)
                return str(e)
    return inner


def session_decorator(func):
    """Декоратор для выдачи сессий на функции"""
    @wraps(func)
    async def inner(*args, **kwargs):
        with BaseSession() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as e:
                session.rollback()
                print(e)
                return str(e)
    return inner


@session_decorator
async def create_product(product: schemas.Product, session: AsyncSession = None) -> models.Product:
    """Создание задачи. Возвращает объект задачи"""
    product = models.Product(**product.model_dump())
    session.add(product)
    session.commit()
    # await session.commit()
    return product


@session_decorator
async def get_products(session: AsyncSession = None) -> list[models.Product]:
	"""Возвращает данные для всех продуктов"""
	query = select(models.Product)
	result = session.execute(query)
	return result.scalars().all()


@session_decorator
async def get_product_by_id(id: int, session: AsyncSession = None) -> models.Product:
	"""Возвращает данные для всех продуктов"""
	return session.get(models.Product, id)


@session_decorator
async def get_products_by_type(type_id: int, session: AsyncSession = None) -> list[models.Product]:
	"""Возвращает данные для всех продуктов"""
	query = (
		select(models.Product)
		.where(models.Product.product_type_id == type_id)
	)
	result = session.execute(query)
	return result.scalars().all()