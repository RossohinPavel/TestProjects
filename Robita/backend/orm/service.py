from tortoise import Tortoise
from schemas import User as UserSchema
from orm.settings import TORTOISE_CONFIG
from orm.models import User


def connection(func):
	"""Декоратор для подключения к базе данных"""
	async def wrapper(*args, **kwargs):
		await Tortoise.init(
			db_url=TORTOISE_CONFIG['connections']['default'],
			modules={'models': TORTOISE_CONFIG['apps']['models']['models']}
		)
		await Tortoise.generate_schemas()
		res = None
		try:
			res = await func(*args, **kwargs)
		except:
			pass
		await Tortoise.close_connections()
		return res

	return wrapper


@connection
async def create_user(user: UserSchema):
	"""Создание пользователя"""
	record = await User.create(
		telegram_id = user.telegram_id,
		first_name = user.first_name,
		last_name = user.last_name,
		username = user.username,
		birth_date = str(user.birth_date)
	)
	await record.save()


@connection
async def get_user(telegram_id: int) -> UserSchema:
	"""Получение пользователя"""
	user = await User.get(telegram_id=telegram_id)
	user_schema = UserSchema(
		telegram_id = user.telegram_id,
		first_name = user.first_name,
		last_name = user.last_name,
		username = user.username,
		birth_date = user.birth_date.date()
	)
	return user_schema
