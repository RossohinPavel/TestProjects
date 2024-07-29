import telebot
import modules.app_manager as APP


# Непосредственно, бот!)
BOT = telebot.TeleBot('', skip_pending=True)


from . import orders
from . import tasks


def send_help_message(chat_id: int | str, _: str | None = None) -> None:
    """Посылает сообщение с подсказкой."""
    msg = (
        'Привет! Я Бот-Помощник. Вводи команды и следуй инструкциям. Для быстрого доступа к коммандам есть меню у клавиатуры.',
        'Доступные команды:',
        '/order - Получить информацию по заказу.',
        '/new_task - Добавить задачу.',
        '/tasks - Вывести список задач.'
    )
    BOT.send_message(chat_id=chat_id, text='\n'.join(msg))


COMMAND = None
COMMANDS = {
    '/start': send_help_message,
    '/help': send_help_message,
    '/order': orders.request_an_order_number,
    '/new_task': tasks.request_task_name,
    '/tasks': tasks.cmd_show_tasks_keyboard
}


@BOT.callback_query_handler(func=lambda _: True)
def callback_handler(call: telebot.types.CallbackQuery):
    """
    Обработка нажатий на кнопки в меню.
    Команда - форматированный запрос, сохраненный в call.data. Он имеет следующий синтаксис
    -<символ модуля><символ команды> <аргумнеты>. Пример: '-ob 250501'
    - (Тире) служит маркером поступающей комманды
    Следующий за ним символ обозначает модуль, к которому нужно обраться
    t - Модуль, отвечающий за задачи из ТУДУ листа
    o - Модуль заказов
    За символом модуля идет символ команды. Для каждого модуля они свои.
    Их Описание можно найти в ф-ии callback_handler соответствующего модуля
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    match call.data[:2]:
        case '-t': module = tasks
        case '-o': module = orders
        case _: module = None
    
    try:
        module.callback_handler(chat_id, message_id, call.data[2:])
    except Exception as e:
        BOT.send_message(chat_id=chat_id, text=f'<{module.__name__}>' + '\n' + str(e))


@BOT.message_handler(content_types=['text'])
def message_handler(message: telebot.types.Message) -> None:
    """Обработка сообщений бота"""
    global COMMAND
    msg = message.text
    chat_id = message.chat.id

    if msg in COMMANDS:
        COMMANDS[msg](chat_id, msg)
        return
    
    if COMMAND:
        COMMAND(chat_id, msg)
        COMMAND = None


@APP.THREAD_MANAGER.parallel
def main(token: str) -> None:
    """Запуск телебота"""
    match token:
        case 'stop':
            BOT.stop_bot()
        case _:
            BOT.token = token
            BOT.polling(non_stop=True, skip_pending=True)
