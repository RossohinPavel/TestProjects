from ..data_base import DataBase
from .data_classes import Order, Edition, Photo
from ..library.main import Library
from typing import Any, Generator


Library = Library()


class Log(DataBase):
    """Класс предостовляющий доступ к чтению лога заказов"""
    __slots__ = ()

    data_base = 'log.db'

    # Сохраняем классы для доступа к типизации
    Order = Order
    Edition = Edition
    Photo = Photo

    @DataBase.safe_connect
    def get(self, order_name: str) -> Order | None:
        """Получение объекта заказа из лога."""
        self.cursor.execute('SELECT * FROM Orders WHERE name=?', (order_name, ))
        res = self.cursor.fetchone()
        if res: 
            return Order(*res[1:], self.__get_photos(order_name), self.__get_editions(order_name))  #type: ignore
    
    def __get_photos(self, order_name: str) -> tuple[Photo, ...]:
        """Вспомогательная ф-я для получения информации о фотопечати в заказе"""
        self.cursor.execute('SELECT name, value FROM Photos WHERE order_name=?', (order_name, ))
        return tuple(Photo(*r) for r in self.cursor.fetchall())

    def __get_editions(self, order_name: str) -> tuple[Edition, ...]:
        """Вспомогательная ф-я для получения информации о тиражах в заказе"""
        self.cursor.execute(
            """
                SELECT name, covers, pages, ccount, comp 
                FROM Editions 
                WHERE order_name=?
            """, 
            (order_name, )
        )
        # Жеский однострочечник)) Создаем tuple из объектов Edition
        # Запрос вернет 5 элементов, которые соответствуют порядку атрибутов в Edition
        # 6 атрибут -  продукт из библиотеки
        return tuple((Edition(*e, Library.get(e[0])) for e in self.cursor.fetchall()))    # type: ignore

    @DataBase.safe_connect
    def get_newest_order_name(self) -> str:
        """Получение последнего сканированного номера заказа"""
        self.cursor.execute('SELECT MAX(name) FROM Orders')
        return self.cursor.fetchone()[0]
