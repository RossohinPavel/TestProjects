# Импорты необходимые для работы самого Обработчика
import modules.app_manager as APP
from .._grabbers import EditionGrabber


# Импорты необходимые для работы дочерних классов по обработке изображений
from math import ceil as m_ceil
from os import makedirs as os_makedirs
from PIL import Image, ImageDraw, ImageFont


class Handler:
    """Абстрактный класс предостовляющий реализующий основную логику обработчиков"""
    __slots__ = '__name__', 'order_name', 'option', 'assist', 'source', 'destination', 'files'

    types: tuple[str, ...] = ()             # Кортеж типов продуктов, на работу с которыми расчитан обработчик
    grabber_mode: tuple[str, ...] = ()      # Режим, в котором работает EditionGrabber. Свой для каждого обработчика

    def __init__(self) -> None:
        self.__name__ = self.__class__.__name__
        # Переменная для хранения имени заказа
        self.order_name: str
        
        # Маркер дополнительной опции обработки
        self.option: bool = False

        # Переменные пути
        self.source: str                        # Переменная для хранения пути, источника файлов
        self.destination: str                   # Переменная для хранения пути назначения

        # Вспомогательный атрибут
        self.assist = {}
        
        # Список для хранения файловых объектов
        self.files: list[EditionGrabber | None] = []   

    @staticmethod
    def mm_to_pixel(mm: int | float) -> float:
        """Возвращает значение в пикселях при разрешении в 300 dpi."""
        return mm * 11.811

    def _update_files(self, order: APP.log.Order) -> None:
        """
            Итерируется по тиражам и наполняет список self.files объектами EditionGrabber.
            Добавлет этот объект, если для тиража есть определившийся продукт, 
            в остальных случаях - добавляет None.
        """
        for edition in order.content:
            file_obj = None

            if edition.product and edition.product.type in self.types:
                file_obj = EditionGrabber(f'{self.source}/{edition.name}', *self.grabber_mode)  # type: ignore
                
            self.files.append(file_obj)

    def get_total_sum_of_images(self) -> int:
        """В дочернем классе должна возвращать сумму изображений"""
        raise Exception('Функция get_total_sum_of_images должна быть переопределена в дочернем классе')
    
    def get_handler_header(self, order_name: str) -> str:
        """Возварщает заголовок, который будет использоваться в процессинг фрейме."""
        return f'Обработка {order_name}'

    def __call__(self, order: APP.log.Order, option: bool) -> None:
        # Общая конфигурация прокси объекта
        APP.pf.header.step(self.get_handler_header(order.name))
        APP.pf.operation.step('Подготовка изображений')

        # Устанавливаем имя заказа
        self.order_name = order.name

        # Обновляем маркер дополнительной обработки
        self.option = option

        # Получаем ссылки на диск-источник и диск, с которого идет печать.
        tail = f'{order.creation_date}/{order.name}'
        self.source = f'{APP.stg.z_disc}/{tail}'
        self.destination =  f'{APP.stg.o_disc}/{tail}'

        # Обновляем Обработчик. Наполняем список files.
        self._update_files(order)

        # Конфигурация Процессинг фрейма
        APP.pf.operation.reset()
        APP.pf.operation.maximum = sum(1 for f in self.files if f)
        APP.pf.filebar.maximum(self.get_total_sum_of_images())

        # Старт основной логики обработки
        for i, file_grabber in enumerate(self.files):
            # Запускаем функцию обрабочика, если есть файловый объект тиража 
            # (соответственно и продукт для этого тиража).
            if file_grabber:
                edition = order.content[i]
                APP.pf.operation.step(edition.name)
                self.handler_run(edition, file_grabber)

        # Сброс значений
        self._reset_to_default()

    def handler_run(self, edition: APP.log.Edition, file_grabber: EditionGrabber) -> None:
        """Запускает основную логику обработчика файлов"""
        raise Exception('Функция handler_run должна быть переопределена в дочернем классе')
    
    def _reset_to_default(self) -> None:
        """Сброс значений на начальные"""
        self.source = self.destination = self.order_name = ''
        self.assist.clear()
        self.files.clear()
