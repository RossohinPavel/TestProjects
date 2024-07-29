"""
    Инициализация чистого лог-файла
"""

import sqlite3


def create_clear_log():
    with sqlite3.connect('../../data/log.db') as log:
        log.cursor().execute(
            """CREATE TABLE Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            creation_date TEXT,
            customer_name TEXT,
            customer_address TEXT,
            price REAL
            )"""
        )
        log.cursor().execute(
            """CREATE TABLE Editions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_name TEXT,
            name TEXT,
            covers INT,
            pages INT,
            ccount TEXT,
            comp TEXT
            )"""
        )
        log.cursor().execute(
            """CREATE TABLE Photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_name TEXT,
            name TEXT,
            value INT
            )"""
        )
        # log.cursor().execute(
        #     """INSERT INTO Orders 
        #     (name, creation_date, customer_name, customer_address, price)
        #     VALUES (?, ?, ?, ?, ?)""", 
        #     ('000000', '2020-01-01', 'Admin', 'Home', 66.6)
        # )
        # log.cursor().execute(
        #     """INSERT INTO Editions 
        #     (order_name, name, covers, pages, ccount, comp)
        #     VALUES (?, ?, ?, ?, ?, ?)""", 
        #     ('000000', 'Test-Фотопечать SRA3 170гр горизонт 40', 1, None, None, None)
        # )


if __name__ == '__main__':
    create_clear_log()
