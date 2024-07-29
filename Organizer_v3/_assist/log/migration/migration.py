"""
    Осуществляет миграцию записей из старой базы данных в новую.
    Принудительно сортирует записи по имени заказа
"""
import sqlite3


def main():
    with sqlite3.connect('../../../data/log.db') as current_con, sqlite3.connect('log_15_12_2023.db') as old_con:
        current_cursor = current_con.cursor()
        old_cursor = old_con.cursor()

        # Переливаем информацию по заказам
        old_cursor.execute(
            """
            SELECT name, creation_date, customer_name, customer_address, price 
            FROM Orders
            """
        )
        current_cursor.executemany(
            """
            INSERT INTO 
            Orders (name, creation_date, customer_name, customer_address, price) 
            VALUES (?, ?, ?, ?, ?)
            """, 
            sorted(old_cursor.fetchall(), key=lambda x: x[0])
        )
        
        # Переливаем информацию по тиражам
        old_cursor.execute(
            """
            SELECT order_name, name, covers, pages, ccount, comp 
            FROM Editions
            """
        )
        for on, name, cov, pages, cc, comp in sorted(old_cursor.fetchall(), key=lambda x: x[0]):
            if pages == 0: 
                pages = None

            current_cursor.execute(
                """
                INSERT INTO 
                Editions (order_name, name, covers, pages, ccount, comp) 
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (on, name, cov, pages, cc, comp)
            )
        
        # Переливаем информацию по фотопечати
        old_cursor.execute('SELECT order_name, name, count FROM Photos')
        for on, n, v in  sorted(old_cursor.fetchall(), key=lambda x: x[0]):
            n = n.split()

            match n[1]:
                case 'Gl': n[1] = 'Глянцевая'
                case 'Mt' | _: n[1] ='Матовая'

            current_cursor.execute(
                """INSERT INTO Photos (order_name, name, value) VALUES (?, ?, ?)""",
                (on, ' '.join(n[1:]), v)
            )


if __name__ == '__main__':
    main()
