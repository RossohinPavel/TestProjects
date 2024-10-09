from fastapi import FastAPI
from uvicorn import run

from .products.router import router as products_router
from . import configs


app = FastAPI(**configs.app_configs)
app.include_router(products_router, prefix='/products')


def from_poetry():
	"""Запуск приложения под poetry"""
	run('src.main:app', host='127.0.0.1', port=8000, reload=True)
