"""
    Скрипт для тестирования записей лога.
    Находит заказы, не связанные с тиражами и наоборот, 
    тиражи, не связанные с заказами.
"""
from sqlite3 import connect


DATA_BASE = '../../data/log.db'


def main():
    with connect(DATA_BASE) as log:
        cursor = log.cursor()

        # Получаем общее множество заказов
        cursor.execute(
            """
            SELECT name
            FROM Orders
            """
        )
        orders_set = set((x[0] for x in cursor.fetchall()))

        # Получаем Множество имен заказов среди тиражей
        cursor.execute(
            """
            SELECT order_name
            FROM Editions
            """
        )
        order_names_from_edt = set((x[0] for x in cursor.fetchall()))

        # Получаем Множество имен заказов среди фотопечати
        cursor.execute(
            """
            SELECT order_name
            FROM Photos
            """
        )
        order_names_from_photo = set((x[0] for x in cursor.fetchall()))

        non_ordered_editions = order_names_from_edt - orders_set
        print('Тиражи, не связанные с заказами:', len(non_ordered_editions))
        if non_ordered_editions:
            print(non_ordered_editions)

        non_ordered_photos = order_names_from_photo - orders_set
        print('Фотопечать, не связанные с заказами:', len(non_ordered_photos))
        if non_ordered_photos:
            print(non_ordered_photos)

        empty_orders = orders_set - order_names_from_edt - order_names_from_photo
        print("Пустые заказы:", len(empty_orders))
        if empty_orders:
            print(empty_orders)


if __name__ == '__main__':
    main()
