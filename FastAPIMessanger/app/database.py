from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from os import getenv


class Connection:
    """КМ для подключения к mongo"""
    URI = f'mongodb://{getenv('MONGO_INITDB_ROOT_USERNAME')}:{getenv('MONGO_INITDB_ROOT_USERNAME')}@mongo:27017'

    async def __aenter__(self):
        self.client = AsyncIOMotorClient(self.URI, server_api=ServerApi('1'))
        self.database = self.client['messages_database']
        self.collections = self.database['messages']
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(exc_type, exc_val, exc_tb)


async def save_message(message: dict):
    """Сохраняет сообщение в базе данных"""
    async with Connection() as c:
        res = await c.collections.insert_one(message)
    return res


async def get_messages():
    """Достает изображения из базы данных"""
    async with Connection() as c:
        cursor = c.collections.find()
        return cursor
