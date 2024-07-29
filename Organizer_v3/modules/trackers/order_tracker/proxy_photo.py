from .proxy import FileObserver, Any
from ...file_handlers._iterators import photo_iterator


class PhotoProxy(FileObserver):
    """Объект слежения за фотопечатью"""

    # Указание названи таблицы
    table = 'Photos'

    def __init__(self, order_proxy, proxy_name, name: str) -> None:
        super().__init__(order_proxy, proxy_name, name)

    def _update_info(self):
        """Ф-я подсчета фотопечати в заказе."""
        # Промежуточный словарь для сравнения значений
        dct = {}

        # Итерируемся по фотопечати в заказе
        for paper, size, pages_it in photo_iterator(self._path):
            # Отсекаем слово Фото из имени
            size = size.split(maxsplit=1)[1]

            # Получаем строку формата и мультипликатор изображений
            size, multiplier = size.split('--')

            # Обновляем значения словаря
            multiplier = int(multiplier)
            name = f'{paper} {size}'

            if name not in dct:
                dct[name] = 0
            dct[name] += sum(multiplier for _ in pages_it)

        # помещаем атрибуты на объект
        for k, v in dct.items(): 
            self[k] = v
    
    def check_request(self, name: str) -> str:                              #type: ignore
        req = f"""
        SELECT EXISTS (
            SELECT name 
            FROM Photos 
            WHERE order_name=\'{self._order_proxy.name}\'
            AND name=\'{name}\' 
            LIMIT 1
        )"""
        return req
    
    def insert_request(self, name: str) -> tuple[str, tuple[Any, ...]]:    #type: ignore
        req = f"""
        INSERT INTO 
        Photos (order_name, name, value) 
        VALUES (?, ?, ?)
        """
        return req, (self._order_proxy.name, name, getattr(self, name))
    
    def update_request(self, name: str) -> tuple[str, tuple[Any, ...]]:         #type: ignore
        req = f"""
        UPDATE Photos 
        SET value=? 
        WHERE order_name=\'{self._order_proxy.name}\' 
        AND name=\'{name}\'
        """
        return req, (getattr(self, name), )
