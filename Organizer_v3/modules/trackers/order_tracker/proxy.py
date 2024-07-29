from abc import ABC, abstractmethod
from typing import Any


class BaseObserver(ABC):
    """Реализует базовую логику наблюдения за объектом"""
    __slots__ = '_count', '_updated', 'name'

    @abstractmethod
    def __init__(self, name: str) -> None:
        # Атрибуты управления прокси-объектом
        self.name = name
        self._count = 0                     # Счетчик итераций обновления объекта
        self._updated = False               # Метка для обновления
    
    @abstractmethod
    def _update_info(self) -> None:
        """
            Абстракнтый метод установки на объект информации. 
            Этот метод должен вызываться методм update_proxy
        """
        pass

    @abstractmethod
    def update_proxy(self):
        """Логика работы прокси объекта. Его следует вызывать в трекере"""
        pass

    @property
    def check_request(self) -> str:
        """Запрос SQL на проверку дубликата"""
        raise Exception(f'Не переопределен метод check_request')
    
    @property
    def insert_request(self) -> tuple[str, tuple[Any, ...]]:
        """Запрос SQL на добавление в базу данных"""
        raise Exception(f'Не переопределен метод insert_request')

    @property
    def update_request(self) -> tuple[str, tuple[Any, ...]]:
        """Запрос SQL для обновления базы данных"""
        raise Exception(f'Не переопределен метод update_request')

    def __setitem__(self, key: str, value: str | int | float | None):
        """
            Установка значения атрибута на объект. 
            Дополнительно проверяет на совпадение значений.
            Управляет _updated атрибутом объекта.
        """
        if value != getattr(self, key, None):
            self._updated = True
        super().__setattr__(key, value)


class FileObserver(BaseObserver):
    """Реализует логику слежения за файлами: тиражами и фотопечатью"""
    __slots__ = '_order_proxy', '_proxy_name', '_hash', 'name'              

    @abstractmethod
    def __init__(self, order_proxy, proxy_name, name: str) -> None:
        super().__init__(name)
        self._order_proxy = order_proxy         # Ссылка на прокси объект хранения информации о заказе
        self._proxy_name = proxy_name           # Имя прокси объекта
        self._hash = hash(proxy_name)           # переменная для хранения хеш-значения
        self.name = name                        # Имя тиража
    
    @property
    def _path(self) -> str:
        return self._order_proxy._path + '/' + self.name

    def update_proxy(self) -> None:
        # Когда сетчик равен 0, вызываем сканирование объекта
        if self._count == 0:
            self._updated = False
            self._update_info()
        
        # Если после обновления атрибут _updated остался False, это значит, что новая информация равна старой.
        # В таком случае, можно увеличить счетчик и пропускать сканирование объекта.
        if not self._updated:
            self._count += 1
        
        # Каждые 20 минут (Цикл трекера - 150 секунд, 8 итераций -> 20 минут)
        # Устанавливаем метки на начальное положение для инициализации повтороного сканирования.
        if self._count == 8:
            self._count = 0

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, _value: object) -> bool:
        if isinstance(_value, str):
            return self._proxy_name == _value
        return _value._hash == self._hash       #type: ignore
