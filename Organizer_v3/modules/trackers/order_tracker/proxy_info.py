from re import findall
from .proxy import BaseObserver, Any


class OrderInfoProxy(BaseObserver):
    """
        Объект слежения за файлом completed.htm содержащий в себе информацию о заказе.
        Повторяет некоторые эдементы ProxyObserver для получения общего интерфейса.
    """

    # Паттерны для re для распознавания информации
    _patterns = {
        'customer_name': r'Уважаемый \(ая\), (.+) !</p>',
        'customer_address': r'выдачи.+\n?.+\n?.+<strong>(.+)</strong>',
        'price': r'руб\..+<strong>(\d+\.?\d*)'
    }

    __slots__ = 'name', 'creation_date', 'customer_name', 'customer_address', 'price', '_path'                      

    def __init__(self, z_disc: str, day: str, order: str) -> None:
        super().__init__(order)
        # Информационные атрибуты
        self.creation_date = day                        # Дата создания заказа
        self.customer_name = '_unknown_'                # Имя заказчика
        self.customer_address = '_unknown_'             # Адрес заказчика
        self.price = 0.0                                # Общая стоимость заказа

        # Атрибуты управления объектом
        self._path = f'{z_disc}/{day}/{order}'          # Полный путь до объекта

        # Флаг _updated и счетчик _count будет работать в этом прокси слегка по-другому.
        # Помимо обновления, _updated будет служить флагом присутствия заказа в библиотеке.
        # Объект, в отличие от родительского, создаем с True значением. Заказ должен попасть
        # в бибилотеку в любом случае, есть в нем информация, или там значения по-умолчанию.
        self._updated = True

    def update_proxy(self) -> None:
        # self._count будет служить меткой от повторного записи в библиотеку
        # Если его значение равно 0 - пытаемся получить информацию из completed.htm
        if not self._count:
            try:
                self._update_info()
                # Повторно сканировать существующий completed нет необходимости.
                # Поэтому, при успехе меняем _count на 1, и _updated снова на True, чтобы объект прошел проверку на запись.
                self._count = 1
                self._updated = True
            except:
                # В случае ошибки (не найден файл completed), то продолжаем искать его раз за разом.
                # Для большинства заказов он будет найден, остальные остануться со значением по умолчанию
                pass

    def _update_info(self) -> None:
        """Парсим completed.htm с целью нахождения нужной нам информации"""
        with open(f'{self._path}/completed.htm', encoding='utf-8') as file:
            string = file.read()

            # По паттерну находим нужную строку
            for arg, pattern in self._patterns.items():
                res = findall(pattern, string)
                if res:
                    res = res[0]
                    if arg == 'price': 
                        res = float(res)
                    self[arg] = res
    
    @property
    def check_request(self) -> str:
        return f'SELECT EXISTS (SELECT name FROM Orders WHERE name=\'{self.name}\' LIMIT 1)'
    
    @property
    def insert_request(self) -> tuple[str, tuple[Any, ...]]:
        fields = ', '.join(self.__slots__[:-1])
        return f'INSERT INTO Orders ({fields}) VALUES (?, ?, ?, ?, ?)', tuple(getattr(self, x) for x in self.__slots__[:-1])
    
    @property
    def update_request(self) -> tuple[str, tuple[Any, ...]]:
        fields = 'customer_name=?, customer_address=?, price=?'
        return f'UPDATE Orders SET {fields} WHERE name={self.name}', (self.customer_name, self.customer_address, self.price)
