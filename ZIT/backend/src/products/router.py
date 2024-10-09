from fastapi import APIRouter, HTTPException
from . import schemas
from . import service


router = APIRouter(tags=['products'])


@router.get('/{id}', status_code=200)
async def get_product(id: int) -> schemas.ProductModel:
	"""Получение товара по id"""
	result = await service.get_product_by_id(id)
	if result is None:
		raise HTTPException(status_code=404, detail='Item not found')
	return result


@router.get('/', status_code=200)
async def get_products() -> list[schemas.ProductModel]:
	"""Получение списка всех товаров"""
	return await service.get_products()


@router.get('/type/{type_id}', status_code=200)
async def get_products_by_type(type_id: int) -> list[schemas.ProductModel]:
	"""Получение списка всех товаров по указанному типу"""
	return await service.get_products_by_type(type_id)


@router.post('/', status_code=201)
async def create_product(product: schemas.Product) -> schemas.ProductModel:
	"""Добавление нового товара"""
	product = await service.create_product(product)
	try:
		return schemas.ProductModel.model_validate(product, from_attributes=True)
	except Exception as e:
		return {'message': str(e)}
