from pydantic import BaseModel
from typing import Union


class ProductType(BaseModel):
	id: int
	name: str


class Product(BaseModel):
	"""Pydantic-представление продукта для POST-запроса"""
	name: str
	product_type_id: int


class ProductModel(BaseModel):
	"""Pydantic-представление продукта для GET-запроса"""
	id: int
	name: str
	product_type: Union['ProductType', None]
