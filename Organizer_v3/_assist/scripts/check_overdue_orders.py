"""
    Скрипт для выявления просроченных заказов. 
    Фильтрует информацию на момент запуска фильтра. (системное время)
    Формирует 2 поля - просроченные заказы и горящие заказы 
    (срок исполнения которых меньше 1 дня)
    Работает с текстовым документом, который был экспортирован из ASC Control.
"""
from datetime import datetime, timedelta


FORMAT = r'%d.%m.%Y %H:%M:%S'

NOW = datetime.now()
DELTA_4 = timedelta(days=4)
DELTA_3 = timedelta(days=3)

INDENTS = [0] * 10 

ORDERS = {'overdue': [], 'hot': [], 'normal': []}
HEADERS = {
    'overdue': '----- Просроченные заказы -----\n', 
    'hot': '\n----- Заказы, которые должны быть скоро готовы -----\n', 
    'normal': '\n----- Заказы в работе -----\n',
    'first_line': None
}

STATUSES = ('В печати', 'Отпечатан', 'На упаковке')


def convert_line(line: list[str]) -> None:
    """Выравнивает строки в списке line по значениям INDENTS"""
    for i, value in enumerate(line):
        line[i] = value.ljust(INDENTS[i] + 4)


def sort_line(line: list[str]) -> None:
    """Распределяет строки между списками"""
    diff = NOW - datetime.strptime(line[1], FORMAT)

    if diff > DELTA_4:
        ORDERS['overdue'].append(line)
        return

    if DELTA_3 <= diff <= DELTA_4:
        ORDERS['hot'].append(line)
        return
    
    ORDERS['normal'].append(line)


with open('OrdersReport.txt', 'r', encoding='cp1251') as file:
    lines = file.readlines()


for line in lines:
    line = line[:-2].split('\t')

    # Разбираем линию по статусу
    status = line[-2]
    if status in STATUSES or status == 'Текущий статус':
        # Убираем ненужные столбики и формируем длинну отступов
        line.pop(1)
        line.pop(-1)
        line.pop(-2)

        for i, value in enumerate(line):
            str_len = len(value)
            if str_len > INDENTS[i]:
                INDENTS[i] = str_len
    
    if status == 'Текущий статус':
        HEADERS['first_line'] = line
    
    if status in STATUSES:
        sort_line(line)


with open('result.txt', 'w', encoding='utf-8') as file:
    # Выравниваем столбики в строчке заголовков
    convert_line(HEADERS['first_line'])
    HEADERS['first_line'].append('\n')

    for key, lst in ORDERS.items():
        # Пишем заголовки 
        file.write(HEADERS[key])
        file.writelines(HEADERS['first_line'])

        # Пишем значения
        for line in lst:
            convert_line(line)
            line.append('\n')
            file.writelines(line)
