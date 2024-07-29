"""
Представьте, что у вас есть таблица users в базе данных SQLite с полями id, name, и age. 
Напишите Python-скрипт, который подключается к этой базе данных, выбирает всех пользователей старше 30 лет и выводит их имена и возраст.
Ваш код здесь
"""
import sqlite3


BASE = 'db.sqlite'


def create_table():
    """Создание таблицы для задания"""
    with sqlite3.connect(BASE) as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            CREATE TABLE users
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
            """
        )


def insert_test_data():
    """Добавление тестовых данных"""
    people = [
        ('Evelyn Rodriguez', 42), ('Alexander Brown', 31), ('Sophia Patel', 25), 
        ('Julian Lee', 48), ('Ava Martin', 38), ('Liam Hall', 29), ('Emily Chen', 22), 
        ('Jackson Kim', 55), ('Olivia White', 41), ('Benjamin Taylor', 39)
    ]
    with sqlite3.connect(BASE) as connect:
        cursor = connect.cursor()
        cursor.executemany(
            """
            INSERT INTO users (name, age)
            VALUES (?, ?)
            """,
            people
        )
        connect.commit()


def do_select_query():
    """Выполнение запроса на выборку данных по заданию"""
    with sqlite3.connect(BASE) as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            SELECT name, age
            FROM users
            WHERE age > 30
            """
        )
        print(*cursor.fetchall(), sep='\n')
