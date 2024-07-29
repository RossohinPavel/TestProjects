import os
from re import fullmatch
from typing import Literal, Iterator


# Паттерны для проверки модулем re
DAY_PATTERN = r'\d{4}(-\d{2}){2}'
ORDER_PATTERN = r'\d{6}'
IMG_SAMPLE = r'(cover|\d{3})_{1,2}(\d{3}|-?\d+_pcs){1,2}\.jpg'
EXEMPLAR = r'\d{3}(-\d+_pcs)?'


it_mode = Literal['Exemplar', 'Constant', 'Covers', 'Variable']


def ot_iterator(path: str) -> Iterator[tuple[str, str, Iterator[str]]]:
    """
        Итератор по номерам заказов, дате их создания и содержимому заказов. 
        Возвращает значения в виде кортежа: (<дата создания>, <имя заказа>, (<Генератор по содержимому>)).
        Генератор по содержимому возвращает имена папок.
        Значения возвращаются в обратном порядке. От новых к старым.
    """

    for day in reversed(os.listdir(path)):
        if fullmatch(DAY_PATTERN, day):
            for order in reversed(os.listdir(f'{path}/{day}')):
                if fullmatch(ORDER_PATTERN, order):
                    order_path = f'{path}/{day}/{order}'
                    it = (x for x in os.listdir(order_path) if os.path.isdir(f'{order_path}/{x}'))
                    yield day, order, it


def photo_iterator(path: str) -> Iterator[tuple[str, str, Iterator[str]]]:
    """Итератор по фотопечати в указаном заказе"""

    paper_path = f'{path}/_ALL/Фотопечать'

    # Прерываем итерацию, если такой папки не существует
    if not os.path.exists(paper_path): return StopIteration

    for paper in os.listdir(paper_path):
        for format in os.listdir(f'{paper_path}/{paper}'):
            yield paper, format, (x for x in os.listdir(f'{paper_path}/{paper}/{format}'))


def edition_iterator(path: str, *mode: it_mode)-> Iterator[tuple[str, Iterator[str]]]:
    """
        Предоставляет итератор по именам каталогов и именам файлов в тираже.
        Возвращает значения в виде кортежа, (<имя каталога>, итератор по именам файлов)
    """

    ex = 'Exemplar' in mode
    for catalog in os.listdir(path):
        c_path = f'{path}/{catalog}'
        if ex and fullmatch(EXEMPLAR, catalog) or catalog in mode:
            yield catalog, (name for name in os.listdir(f'{c_path}') if fullmatch(IMG_SAMPLE, name))
