from telethon import TelegramClient
import asyncio
import os
import threading


# Папка для сообщений
if not os.path.exists('Messages'):
    os.mkdir('Messages')


# Получение настроек телеграм клиента из окружения.
TG_API_ID = os.getenv('TG_API_ID')
TG_API_HASH = os.getenv('TG_API_HASH')

# Словарик для хранения объектов-клиентов Телеги
CLIENTS: dict[str, TelegramClient] = {}

# Ссылка на цикл, для запуска в синхронном режиме. 
# Использовать ф-ю run_until_complete, например.
LOOP = asyncio.get_event_loop()
LOOP.run_in_executor

# Статусы возрата для чек ф-ии
ERROR = 'error'
LOGINED = 'logined'
WAITTING = 'waiting_qr_login'


def login(phone: str):
    """Логин пользователя по переданному телефону"""
    if check(phone) == ERROR:
        LOOP.run_until_complete(_await_client(phone))


async def _await_client(phone: str):
    """Создает объект клиента и конектит его."""
    c = TelegramClient(phone, TG_API_ID, TG_API_HASH)
    await c.connect()
    CLIENTS[phone] = c


def check(phone: str) -> str:
    """Проверка статуса логина."""
    if phone not in CLIENTS:
        return ERROR
    
    client = CLIENTS[phone]
    # Проверка на ожидание кода не совсем правильная. 
    # Если мы что-то ожидаем, так это qr. Не дружелюбно ко множеству пользователей.
    if LOOP.is_running() or not LOOP.run_until_complete(client.is_user_authorized()):
        return WAITTING

    if LOOP.run_until_complete(client.is_user_authorized()):
        return LOGINED
    
    return ERROR


def logout(phone: str) -> str:
    """Логаут))"""
    if phone not in CLIENTS:
        raise Exception('User not logined')
    
    LOOP.run_until_complete(CLIENTS[phone].log_out())
    CLIENTS.pop(phone, None)
    return 'logout success'


def get_token(phone: str) -> tuple[str, str|None]:
    """
        Возвращает статус подключения и токен, если ожидается авторизация.
        Инициализирует поток ожидания скана qr кода.
    """
    status = check(phone)
    qr_token = None

    if status == WAITTING:
        qr_login = LOOP.run_until_complete(CLIENTS[phone].qr_login())
        qr_token = qr_login.url
        # Будем ждать скан qr в фоне 5 минут
        t = threading.Thread(
            target=LOOP.run_until_complete, 
            args=(qr_login.wait(120), ),
            daemon=True
        )
        t.start()

    return status, qr_token


def send_message(text: str, from_phone: str, username: str):
    """Посылает сообщение пользователю"""
    client = CLIENTS[from_phone]
    LOOP.run_until_complete(client.send_message(username, text))


def get_messages(phone: str, uname: str, save: bool):
    """Получает сообщения пользователя"""
    client = CLIENTS[phone]
    msgs = LOOP.run_until_complete(client.get_messages(uname, 50))
    if msgs is None:
        raise Exception('No messages')
    
    if save:
        threading.Thread(target=_save, args=(msgs, )).start()

    if isinstance(msgs, list):
        converted_msgs = (_convert(m) for m in msgs)
    else:
        converted_msgs = (_convert(msgs), )
    
    return converted_msgs


def _convert(msg) -> dict:
    """Конвертирует объекты в нужный формат"""
    return {'username': msg.sender.username, 'is_self': msg.out, 'message_text': msg.message}


def _save(msgs):
    """Сохранение сообщений в файл"""
    if not isinstance(msgs, list):
        msgs = [msgs]

    chat = msgs[0].sender.username
    with open(f'Messages/{chat}', 'w', encoding='utf-8') as file:
        file.writelines((f'{m.sender.username}: {m.message}\n' for m in msgs))
