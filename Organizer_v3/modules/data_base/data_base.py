from sqlite3 import connect, Connection, Cursor
from threading import Lock


class DataBase:
    """Реализует общую логику работы с базами данных sqlite3"""
    __slots__ = ()

    # Имя базы данных, к которой будет совершено подключение
    data_base = 'None'

    # Ссылка на объект подключения к базе данных
    connect: Connection = None      #type: ignore

    # Ссылка на объект cursor
    cursor: Cursor = None           #type: ignore

    # Ссылка на Замок, для предотвращения единовременного доступа к бд
    __lock = None

    def __new__(cls):
        # Определяем атрибуты для классов наследников
        if cls.__lock is None:
            cls.connect = connect(f'data/{cls.data_base}', check_same_thread=False)
            cls.cursor = cls.connect.cursor()
            cls.__lock = Lock()

        return super().__new__(cls)

    @staticmethod
    def safe_connect(func):
        """Декоратор для безопасного подключения к бд"""
        
        def wrapper(self, *args, **kwargs):
            with self.__lock:
                return func(self, *args, **kwargs)

        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper
