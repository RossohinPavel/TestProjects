"""Скрипт для обработки запросов бота"""
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dotenv import load_dotenv
from pathlib import Path
from os import getenv
import asyncio


class EnvConfig:
	"""Класс для работы с env - конфигами"""
	dotenv_path = Path(__file__).parent.parent / '.env'
	BOT_TOKEN = getenv('BOT_TOKEN', None)
	HTTPS_URL = getenv('HTTPS_URL', None)


BOT = Bot(token=EnvConfig.BOT_TOKEN)
DP = Dispatcher()


@DP.message(Command('start'))
async def cmd_start(message: types.Message):
	"""Ответ на команду старт"""
	return await get_message(message)


@DP.message(F.text)
async def init_app(message: types.Message):
	"""Инициализация веб-приложения"""
	return await get_message(message)


async def get_message(message: types.Message):
	text = "Привет.\nНажми на прикрепленную кнопку."
	web_app = types.WebAppInfo(url=EnvConfig.HTTPS_URL)
	kb = InlineKeyboardBuilder()
	kb.button(text='Нажми на меня', web_app=web_app)
	return await message.answer(text, reply_markup=kb.as_markup())


async def main():
	await DP.start_polling(BOT)


if __name__ == '__main__':
	asyncio.run(main())
