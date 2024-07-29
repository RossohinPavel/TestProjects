from .proxy import FileObserver


# Необходимые импорты для работы прокси объекта
from collections import Counter
from re import findall, fullmatch
from ...file_handlers._iterators import edition_iterator


# Типизация
from typing import Any, Iterable


class EditionProxy(FileObserver):
    """Объект слежения за тиражами"""

    __slots__ = 'covers', 'pages', 'ccount', 'comp'
    
    def __init__(self, order_proxy, proxy_name: str, name: str) -> None:
        # Информационные атрибуты
        super().__init__(order_proxy, proxy_name, name)
        self.covers = 0                     # Общее количество обложек в заказе
        self.pages: int | None = None       # Общее количество разворотов в заказе.
        self.ccount: int | None = None      # Комплексный счетчик "Кол-во экз / кол-во разворотв в экз"
        self.comp: int | None = None        # Тип совмещения заказа
        
    def _update_info(self) -> None:
        """Ф-я подсчета изображений в тиражах. Определяет тип совмещения"""
        covers = 0
        page_lst = []
        const = tuple()
        for catalog, images in edition_iterator(self._path, 'Exemplar', 'Constant'):
            if catalog != 'Constant':
                cover_exist = False
                page_count = 0
                for image in images:
                    if image.startswith('cover'):
                        cover_exist = True
                        continue
                    page_count += 1
                if cover_exist:
                    res = findall(r'\d{3}-(\d+)_pcs', catalog)
                    multiplier = int(res[0]) if res else 1
                    covers += multiplier
                    page_lst.extend([page_count] * multiplier)
            else:
                const = images

        # Устанавливаем атрибуты на объект после сканирования
        self['covers'] = covers
        pages = sum(page_lst)
        self['pages'] = pages if pages > 0 else None
        self['ccount'] = self.get_ccount(pages, page_lst)
        self['comp'] = self.get_comparison(covers, pages, const)

    @staticmethod
    def get_ccount(page_count: int, ex_list: list) -> str | None:
        """Метод для формирования комплексного счетчика в формате <30/3 2/4>"""
        if not page_count: return
        return ' '.join(f'{v}/{k}' for k, v in sorted(Counter(ex_list).items(), key=lambda x: (x[1], x[0])))

    @staticmethod
    def get_comparison(cover_count: int, page_count: int | None, const_list: Iterable) -> str | None:
        """
            Метод для определения типа совмещения обложек и блоков.
            Анализ на основе подсчета постоянных изображений.
        """

        # Возвращаем None, если это одна книжка в тираже или счетчик разворотов = 0.
        # Совмещать штучную продукцию нет смысла))
        if not page_count or cover_count == 1: return

        # Вспомогательные переменные для подсчета
        cover_exist = False
        const_page_count = 0

        # Итерируемся по константам. Ищем файл Cover и считаем постоянные развороты.
        for name in const_list:
            if fullmatch(r'cover_\d+_pcs\.jpg', name):
                cover_exist = True
            if fullmatch(r'\d\d\d_\d+_pcs\.jpg', name):
                const_page_count += int(name.split('_')[1])

        # Возвращаем значения, соответствующие подсчету
        if cover_exist and const_page_count == page_count: return "Копии"
        if cover_exist: return 'О_О'
        if const_page_count == page_count: return 'В_О'
        return 'Индивидуально'

    @property
    def check_request(self) -> str:
        return f"""
        SELECT EXISTS(
            SELECT name
            FROM Editions 
            WHERE order_name=\'{self._order_proxy.name}\'
            AND name=\'{self.name}\'
            LIMIT 1
        )"""

    @property
    def insert_request(self) -> tuple[str, tuple[Any, ...]]:
        fields = 'order_name, name, ' + ', '.join(self.__slots__)
        tpl = (self._order_proxy.name, self.name, *(getattr(self, x) for x in self.__slots__))
        return f'INSERT INTO Editions ({fields}) VALUES (?, ?, ?, ?, ?, ?)', tpl

    @property
    def update_request(self) -> tuple[str, tuple[Any, ...]]:
        fields = ', '.join(f'{s}=?' for s in self.__slots__)
        tpl = (self.covers, self.pages, self.ccount, self.comp)
        return f'UPDATE Editions SET {fields} WHERE order_name=\'{self._order_proxy.name}\' AND name=\'{self.name}\'', tpl
