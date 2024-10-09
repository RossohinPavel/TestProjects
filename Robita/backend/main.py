"""Скрипт backend-части приложения. Сохранение и получение данных"""
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import User
from orm import service


app = FastAPI()
router = APIRouter(prefix='/api/v1')


@router.post("/", status_code=201)
async def create_user(user: User):
    """Создание пользователя"""
    await service.create_user(user)
    return user


@router.get("/{telegram_id}", status_code=200)
async def get_user(telegram_id: int):
    """Получение пользователя по telegram_id"""
    res = await service.get_user(telegram_id)
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
    return res


allowed_origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
)

app.include_router(router)