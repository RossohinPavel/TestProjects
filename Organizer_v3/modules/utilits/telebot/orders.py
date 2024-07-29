from . import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.gui.frames.info_frame.info_proxy import OrderInfoProxy


PROXY = None
KEYBOARD = InlineKeyboardMarkup()


def callback_handler(chat_id: int, message_id: int, call_data: str) -> None:
    """Обработчик комманд с клавиатуры"""
    cmd, order_name, sub = call_data.split(' ')

    if order_name != PROXY.order.name:
        cmd = 'b'

    match cmd:
        case 'i': text, kb = update_keyboard_from_edition(sub)
        case 'b' | _: text, kb = update_keyboard_from_proxy()
    
    bot.BOT.edit_message_text(text, chat_id, message_id, reply_markup=kb)


def cmd_get_order_info(chat_id: int | str, order: str) -> None:
    """Получение информации по заказу."""
    proxy = OrderInfoProxy(order)

    if proxy:
        global PROXY
        PROXY = proxy
        text, kb = update_keyboard_from_proxy()
    else:
        text, kb = f'Не могу найти заказ {order}', None
    
    msg = bot.BOT.send_message(chat_id=chat_id, text=text)

    if kb:
        bot.BOT.edit_message_reply_markup(chat_id, msg.id, reply_markup=kb)


def request_an_order_number(chat_id: int | str, _ = None) -> None:
    """Отправка сообщения на запрос номера заказа."""
    bot.COMMAND = cmd_get_order_info
    bot.BOT.send_message(chat_id=chat_id, text='Введите номер заказа')


def update_keyboard_from_edition(sub: str) -> tuple[str, InlineKeyboardMarkup | None]:
    """Обновление клавиатуры и сообщения информацией выбранного тиража."""
    KEYBOARD.keyboard.clear()

    msg = 'Ошибка'

    if sub == 'photo':
        msg = '\n'.join(f'{photo.name}: {photo.value}шт' for photo in PROXY.order.photo)

    if sub.isdigit():
        msg = '\n'.join(PROXY.get_edition_info(PROXY.order.content[int(sub)]))

    KEYBOARD.add(InlineKeyboardButton('К заказу', callback_data=f'-ob {PROXY.order.name} back'))

    return msg, KEYBOARD


def update_keyboard_from_proxy() -> tuple[str, InlineKeyboardMarkup | None]:
    """Обновление сообщения и клавиатуры по PROXY объекту."""
    KEYBOARD.keyboard.clear()

    text = '\n'.join((
        PROXY.order.name,
        f'Заказчик: {PROXY.order.customer_name}',
        f'Адрес доставки: {PROXY.order.customer_address}',
        f'Сумма заказа: {PROXY.order.price}'
    ))

    kb = None
    for i, content in enumerate(PROXY.order.content):
        if kb is None:
            kb = KEYBOARD

        btn_text = content.name
        if len(text) > 26:
            btn_text = btn_text[:27] + '...'

        kb.add(InlineKeyboardButton(btn_text, callback_data=f'-oi {PROXY.order.name} {i}'))

    if PROXY.order.photo:
        if kb is None:
            kb = KEYBOARD
        kb.add(InlineKeyboardButton('Фотопечать', callback_data=f'-oi {PROXY.order.name} photo'))

    return text, kb
