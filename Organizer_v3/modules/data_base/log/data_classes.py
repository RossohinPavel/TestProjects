from typing import NamedTuple
from ..library.product import Product


class Photo(NamedTuple):
    """Инофрмация о фотопечати."""
    name: str                               # Имя тиража
    value: int                              # Счетчик отпечатков


class Edition(NamedTuple):
    """Информация о тираже."""
    name: str                               # Имя тиража
    covers: int                             # Счетчик обложек
    pages: int | None                       # Счетчик разворотов
    ccount: str | None                      # Комплексный счетчик обложек/разворотов
    comp: str | None                        # Тип совмещения тиража (актуально для книг)
    product: Product | None                 # Ссылка на соответствующий этому тиражу продукт


class Order(NamedTuple):
    """Информация о заказе."""
    name: str                               # Имя заказа, он же его номер
    creation_date: str                      # Дата загрузки заказа на сервер
    customer_name: str                      # Имя заказчика
    customer_address: str                   # Адрес заказчика
    price: float                            # Общая сумма заказа
    photo: tuple[Photo, ...]                # Кортеж объектов фотопечати заказа
    content: tuple[Edition, ...]            # Кортеж объектов тиражей заказа
