from . import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules import app_manager as APP
from modules.trackers.task_tracker.task import Task


KEYBOARD = InlineKeyboardMarkup()


"""
Список префиксов-комманд для взаимодействия с задачей
e - execute - Выполнить задачу 
i - info - Получить полную информацию по задаче
s - short - Получить короткую информацию по задаче. Имя + описание
u - update - Получить весь список задач
"""


def callback_handler(chat_id: int, message_id: int, call_data: str) -> None:
    """Обработчик комманд с клавиатуры"""
    cmd, task_name = call_data[0], call_data[2:]

    _task = None

    # Дополнительные действия при командах
    if cmd != 'u':
        _task = get_task_from_name(task_name)
        if _task is None or _task.execution:
            cmd = 'u'
    
    if cmd == 'e':
        _task.execute()
        bot.BOT.send_message(chat_id, text=f'Задача <{_task.name}> выполнена')
    
    # Редактирование текста сообщения, к которому прикреплена клавиатура
    match cmd:
        case 's': 
            msg = _task.name
            if _task.description:
                msg += f'\n{_task.description}'
        case 'i': 
            msg = str(_task)
        case 'u' | 'e': 
            msg = 'Менеджер задач'
        case _: 
            msg = 'None'

    bot.BOT.edit_message_text(msg, chat_id, message_id)
    
    # Редактирование клавиатуры
    match cmd:
        case 'u' | 'e': kb = _update_tasks_keyboard()
        case 's': kb = _update_keyboard_from_task(task_name)
        case 'i': kb = _update_keyboard_from_task(task_name, 's')
        case _: kb = None
    
    if kb: 
        bot.BOT.edit_message_reply_markup(chat_id, message_id, reply_markup=kb)


def cmd_create_task(chat_id: int | str, name: str) -> None:
    """Создать задачу в менеджере задач (туду листе)"""
    if not name: return

    task = Task.new(name)
    task.save()
    end = str(task.end)[:16]

    bot.BOT.send_message(chat_id, f'Добавлена задача: {name}\nВыполнить к: {end}')


def cmd_show_tasks_keyboard(chat_id: int | str, _: str) -> None:
    """Отрисовывает клавиатуру задач."""
    bot.BOT.send_message(chat_id, 'Менеджер задач', reply_markup=_update_tasks_keyboard())


def get_task_from_name(task_name: str):
    """Получение объекта задачи из трекера по имени."""
    for t in APP.TASK_TRACKER.tasks:
        if t.name.startswith(task_name):
            return t


def request_task_name(chat_id: int | str, _ = None) -> None:
    """Запрашивает у пользователя имя задачи. Обновляет COMMAND в bot'е"""
    bot.COMMAND = cmd_create_task
    bot.BOT.send_message(chat_id=chat_id, text='Введите имя задачи')


def _update_keyboard_from_task(name: str, cmd='i') -> InlineKeyboardMarkup:
    """Обновляет клавиатуру кнопками зваимодействия с задачей."""
    KEYBOARD.keyboard.clear()

    btn1 = InlineKeyboardButton('Выполнить', callback_data=f'-te {name}')

    match cmd:
        case 'i': btn2_text = 'Подробнее'
        case 's' | _: btn2_text = 'Коротко'
    btn2 = InlineKeyboardButton(btn2_text, callback_data=f'-t{cmd} {name}')

    btn3 = InlineKeyboardButton('Назад', callback_data='-tu')
    
    KEYBOARD.row(btn1)
    KEYBOARD.row(btn2, btn3)

    return KEYBOARD


def _update_tasks_keyboard() -> InlineKeyboardMarkup:
    """Обновляет клавиатуру, отрисовывая на ней кнопки задач."""
    KEYBOARD.keyboard.clear()

    for task in APP.TASK_TRACKER.tasks:
        if task.execution is None:
            task_name = task.name

            if len(task_name) > 22:
                task_name = task_name[:19] + '...'

            btn = InlineKeyboardButton(task_name, callback_data='-ts ' + task_name[:19])
            # btn = InlineKeyboardButton(task_name, callback_data=f'-ts ')
            KEYBOARD.add(btn)

    update = InlineKeyboardButton('_Обновить_', callback_data='-tu')
    KEYBOARD.add(update)

    return KEYBOARD
