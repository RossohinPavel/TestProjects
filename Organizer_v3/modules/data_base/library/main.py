# Импорты для работы библиотеки
from ..data_base import DataBase
from .product import Product
from . import properties

# Кэш
from functools import lru_cache

# Типизация
from typing import Any


class Library(DataBase):
    """Класс для работы с библиотекой продуктов"""

    data_base = 'library.db'

    Product = Product
    Properties = properties

    @DataBase.safe_connect
    def add(self, product: Product) -> None:
        """Добавление продукта в библиотеку"""
        # Составление запроса sql и обновление бд
        req = ', '.join('?' * len(product))
        self.cursor.execute(f'INSERT INTO Products {product._fields} VALUES ({req})', product)
        self.connect.commit()
        self.by_name.cache_clear()

    @DataBase.safe_connect
    def __by_alias(self, edition_name: str) -> str | None:
        """
            Получение имени продукта (запись name в библиотеке) 
            по передаваемому полному имени тиража
        """
        self.cursor.execute('SELECT * FROM Aliases')
        for alias, name in self.cursor.fetchall():
            if edition_name.endswith(alias):
                return name

    @lru_cache
    @DataBase.safe_connect
    def by_name(self, name: str) -> Product:
        """Получения объекта продукта по передоваемому имени."""
        self.cursor.execute(f'SELECT * FROM Products WHERE name=?', (name, ))
        res = self.cursor.fetchone()
        return Product(*res)
    
    @DataBase.safe_connect
    def delete(self, name: str) -> None:
        """Удаление продукта из библиотеки."""
        # Удаление продукта из библиотеки
        self.cursor.execute(f'DELETE FROM Products WHERE name=?', (name, ))
        # Очитска таблицы псевдонимов от удаляемого продукта
        self.cursor.execute(f'DELETE FROM Aliases WHERE product=?', (name, ))
        self.connect.commit()
        self.by_name.cache_clear()
    
    def get(self, edition_name: str) -> Product | None: 
        """
            Возвращает объект продукта с которым связан тираж, 
            если этот продукт есть в библиотеке.
        """
        res = self.__by_alias(edition_name)
        if res:
            return self.by_name(res)

    @DataBase.safe_connect
    def get_headers(self) -> list[tuple[str, str]]:
        """Получение типов и имен всех существующих в библиотеке продуктов."""
        return self.cursor.execute('SELECT type, name FROM Products').fetchall()
    
    @DataBase.safe_connect
    def get_aliases(self, name: str) -> list[str]:
        """Получение списка псевдонимов продукта"""
        self.cursor.execute('SELECT alias FROM Aliases WHERE product=?', (name, ))
        return self.cursor.fetchall()
    
    @DataBase.safe_connect
    def change(self, name: str, product: dict, aliases: tuple[str]) -> None:
        """Внесение изменений в продукт"""

        # Составление запроса sql и обновление бд продукта
        req = ', '.join(f'{f}=?' for f in product.keys())
        self.cursor.execute(f'UPDATE Products SET {req} WHERE name=\'{name}\'', tuple(product.values()))

        # Обновление псевдониов для продукции
        self.__update_aliases(name, product['name'], aliases)

        self.connect.commit()
        self.by_name.cache_clear()
    
    def __update_aliases(self, old_name: str, new_name: str, aliases: tuple[str]) -> None:
        """Обновление псевдонимов для продукта."""
        # Получаем множество псевдонимов из базы данных
        self.cursor.execute("""SELECT alias FROM Aliases WHERE product=?""", (old_name, ))
        res = set(x[0] for x in self.cursor.fetchall())

        # Рассчитываем псевдонимы для удаления и для добавления
        aliases = set(aliases)                          #type: ignore
        to_del, to_add = res - aliases, aliases - res   #type: ignore
        try:
            if to_del:
                req = ', '.join(repr(x) for x in to_del)
                self.cursor.execute(f"""DELETE FROM Aliases WHERE alias IN ({req}) AND product=?""", (old_name, ))
            
            self.cursor.execute('UPDATE Aliases SET product=? WHERE product=?', (new_name, old_name))

            if to_add:
                self.cursor.executemany('INSERT INTO Aliases (alias, product) VALUES (?, ?)', ((x, new_name) for x in to_add))

        except Exception as e:
            raise Exception(f'Добавляемые псевдонимы не уникальны\n{e}')
