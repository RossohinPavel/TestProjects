from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import database

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis


app = FastAPI()
router = APIRouter(prefix='/api/v1')
redis = aioredis.from_url('redis://redis:6379', encoding='utf-8')
FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


class Message(BaseModel):
    """Представление сообщения"""
    author: str
    content: str


@router.post("/message/")
async def send_message(message: Message):
    """Принимает сообщение"""
    await redis.flushall()
    saved = await database.save_message(message.model_dump())


@router.get("/messages/")
@cache(expire=3600)
async def get_messages() -> list[Message]:
    """Возвращает сообщения"""
    lst = []
    cursor = await database.get_messages()
    while cursor.alive:
        doc = await cursor.next()
        lst.append(Message.model_validate(doc))
    return lst


app.include_router(router)
