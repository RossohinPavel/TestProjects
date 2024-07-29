from re import fullmatch
import os
from time import sleep as time_sleep, time as time_time
from shutil import copy2

DAY_LIMIT = 3
TIMER = 120

SOURCE = 'D:/тест/Book2'
DESTINATION = 'D:/Архив/copy here'

OBSERVING_LIST = []


class Order:
    __slots__ = 'creation_date', 'name', 'status', '__prev_file_len', '__current_file_len'

    def __init__(self, creation_date, name):
        self.creation_date = creation_date
        self.name = name
        self.status = 'traceable'
        self.__prev_file_len = 0
        self.__current_file_len = 0

    def check(self):
        """Функция для подсчета и проверки. Yield'ит строку с относительным путем файла, если его нет в DESTINATION"""
        counter = 0
        for root, dirs, files in os.walk(f'{SOURCE}/{self.creation_date}/{self.name}'):
            for file in files:
                counter += 1
                rel_path = os.path.relpath(f'{root}/{file}', SOURCE)
                if not os.path.exists(f'{DESTINATION}/{rel_path}'):
                    yield rel_path
        self.__prev_file_len = self.__current_file_len
        self.__current_file_len = counter
        if self.__current_file_len == self.__prev_file_len:
            self.status = 'finished'

    def __eq__(self, other):
        """other - строка с именем заказа"""
        if other == self.name:
            return True
        return False


def observing_update():
    """Функция для обновления OBSERVING_LIST.
    Добавляет новые объект заказов для отслеживания, если их там нет.
    Удаляет из него объекты, которые находятся за пределами отслеживаемого временного промежутка.
    """
    print('Сканирую на наличие новых заказов'.ljust(100, ' '), end='\r')
    observing_period = []               # Шаг 1 - формируем отслеживаемый период
    for x in reversed(os.listdir(SOURCE)):
        if fullmatch(r'\d{4}-\d{2}-\d{2}', x):
            observing_period.append(x)
        if len(observing_period) == DAY_LIMIT:
            break
    for day in reversed(observing_period):        # Шаг 2 - Наполняем OBSERVING_LIST объектами заказов
        for order_name in os.listdir(f'{SOURCE}/{day}'):
            if order_name not in OBSERVING_LIST and fullmatch(r'\d{6}', order_name):
                OBSERVING_LIST.append(Order(day, order_name))
    for order_obj in OBSERVING_LIST:    # Шаг 3 - очищаем список от заказов вне временного отрезка
        if order_obj.creation_date not in observing_period:
            OBSERVING_LIST.remove(order_obj)


def init_copy():
    """Инициализация копирования файлов"""
    print('Получаю список файлов'.ljust(100, ' '), end='\r')
    file_list = []
    for order_obj in OBSERVING_LIST:
        if order_obj.status != 'traceable':
            continue
        file_list.extend(order_obj.check())
    print('Создаю каталоги'.ljust(100, ' '), end='\r')
    for dir_name in set('/'.join(x.split('\\')[:-1]) for x in file_list):
        os.makedirs(f'{DESTINATION}/{dir_name}', exist_ok=True)
    file_list_len = len(file_list)
    for file in file_list:
        splited = file.split('\\')
        print(f'Осталось: {file_list_len} файлов ({splited[1]} - {splited[-1]})'.ljust(100, ' '), end='\r')
        copy2(f'{SOURCE}/{file}', f'{DESTINATION}/{file}')
        file_list_len -= 1


if __name__ == '__main__':
    while True:
        start = time_time()
        try:    # Оборачиваем в try, во избежание ошибок сервера
            observing_update()
            init_copy()
        except:
            pass
        timer = int(TIMER - (time_time() - start))
        while timer > 0:
            print(f'Завершено. Ожидаю {timer // 60}:{timer % 60}'.ljust(100, ' '), end='\r')
            time_sleep(1)
            timer -= 1
