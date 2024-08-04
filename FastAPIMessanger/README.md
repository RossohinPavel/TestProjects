# FastAPIMessanger

## Описание

Выполнение тестового задания по развертыванию "месенджера" на FastAPI в связке с aiogram.

- Web приложение на FastApi. Поддерживаются следующие методы.
    * GET 'api/v1/messages/' показывает спосиок всех сообщений
    * POST 'api/v1/message/' позволяет написать сообщение
- Клиентская часть на aiogram.
    * При отправке сообщения боту, сообщение пересылается на сервер.
    * При вооде команды /messages выводит список сообщений.
- Веб-сервер на Nginx
- MongoDB БД для хранения сообщений
- Кеширование сообщений при помощи Redis

## Установка и запуск

1) Склонировать проект
2) В корне проекта создать файл .env и внести в него:
    * MONGO_INITDB_ROOT_USERNAME=\<my_mongodb_username>
    * MONGO_INITDB_ROOT_PASSWORD=\<my_mongodb_password>
    * BOT_TOKEN=\<telegram_bot_token>
3) Установить необходимые контейнеры командой `docker-compose build`
4) Запустить приложений командой `docker-compose up -d`

\*Серверная часть FastAPI доступна в по адресу localhost.
