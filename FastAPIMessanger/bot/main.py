from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import aiohttp
from os import getenv
import asyncio


BOT = Bot(token=getenv('BOT_TOKEN'))
DP = Dispatcher()


@DP.message(Command('messages'))
async def get_messages(message: types.Message):
    """Вывод полученных сообщений"""
    async with aiohttp.ClientSession() as session:
        async with session.get('http://app:8000/api/v1/messages/') as resp:
            data = await resp.json()
            text = '\n'.join(f'{m['author']}: {m['content']}' for m in data)
    await message.answer(text=text)


@DP.message(F.content_type.in_({'text'}))
async def create_message(message: types.Message):
    """На основе сообщения будем создавать сообщения. Автор - отправитель"""
    data = {'author': message.from_user.full_name, 'content': message.text}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://app:8000/api/v1/message/', json=data) as resp:
            if resp.status == 200:
                await message.answer("Сообщение оптравлено")


async def main():
    await DP.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
