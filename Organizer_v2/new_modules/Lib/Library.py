import sqlite3
import new_modules.Lib.ProductCreator as PC


class Library:
    """Класс для работы с базой данных библиотеки продуктов"""
    __instance = None
    __db = None
    __cursor = None
    __products = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__db = sqlite3.connect('data/library.db')
            cls.__cursor = cls.__db.cursor()
            cls.__products = tuple(PC.__dict__[product]() for product in PC.__all__)

        return cls.__instance

    def __del__(self):
        Library.__cursor = None
        Library.__db.close()
        Library.__instance = None

    @classmethod
    def get_product_objects_list(cls) -> tuple:
        """Метод для получения списка объектов продуктов из конструктора"""
        return cls.__products

    @classmethod
    def get_product_object(cls, value: str) -> object:
        """Метод получения объекта продукта из конструктора. Для получения объекта подойдет как русское имя так и
        категория (имя таблицы)"""
        for obj in cls.__products:
            if obj.name == value or obj.category == value:
                return obj

    @classmethod
    def translator(cls, value: str) -> str:
        """Методя для перевода русского имени в категорию и категории в русское имя. Категория используется как
        имя таблицы в бд."""
        for obj in cls.__products:
            if obj.name == value:
                return obj.category
            if obj.category == value:
                return obj.name

    def get_product_names(self) -> dict:
        """Метод возвращает из базы данных имена всех продуктов. Формирует словарь: {тип: (имя1, имя2, ...)}"""
        self.__cursor.execute("SELECT name FROM sqlite_sequence")
        category_lst = tuple(x[0] for x in self.__cursor.fetchall())
        dct = {}
        for category in category_lst:
            self.__cursor.execute(f"SELECT full_name FROM {category}",)
            dct.update({category: tuple(x[0] for x in self.__cursor.fetchall())})
        return dct

    def get_product_values(self, category: str, full_name: str) -> dict:
        """
        Метод для получения данных из бд в виде словаря
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        """
        keys = tuple(self.get_product_object(category).__dict__.keys())
        sql_req = ', '.join(f'\"{x}\"' for x in keys)
        self.__cursor.execute(f'SELECT {sql_req} FROM {category} WHERE full_name=\'{full_name}\'')
        values = self.__cursor.fetchone()
        return {keys[i]: values[i] for i in range(len(keys))}

    def check_unique(self, category: str, full_name: str) -> bool:
        """
        Метод для проверки продукта на дубликат.
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        :return: True если продукта нет в бд и False, если есть.
        """
        self.__cursor.execute(f'SELECT * FROM {category} WHERE full_name=\'{full_name}\'')
        return not self.__cursor.fetchone()

    def add(self, category: str, product_dict: dict):
        """
        Метод добавления продукта в библиотеку
        :param category: Категория продукта / название таблицы
        :param product_dict: Словарь с сформированными значениями
        """
        keys = ', '.join(f'{x}' for x in product_dict.keys())
        values = ', '.join(f'\'{x}\'' if type(x) == str else f'{x}' for x in product_dict.values())
        self.__cursor.execute(f'INSERT INTO {category} ({keys}) VALUES ({values})')
        self.__db.commit()

    def change(self, category: str, full_name: str, values: dict):
        """
        Внесение изменений в ячейку
        :param category:  Категория продукта / название таблицы
        :param full_name: Имя продукта
        :param values: Словарь с новыми значениями
        """
        sql_req = ', '.join(f'{k} = \"{v}\"' if type(v) == str else f'{k} = {v}' for k, v in values.items())
        self.__cursor.execute(f'UPDATE {category} SET {sql_req} WHERE full_name=\'{full_name}\'')
        self.__db.commit()

    def delete(self, category: str, full_name: str):
        """
        Метод для удаления продукта из библиотеки.
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        """
        self.__cursor.execute(f'DELETE FROM {category} WHERE full_name=\'{full_name}\'')
        self.__db.commit()
