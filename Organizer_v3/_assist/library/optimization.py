"""
    Скрипт для 'оптимизации' базы данных.
    Сортирует строки в базе данных по имени продукции
    Сжимает неиспользуемое пространство.
"""
import sqlite3


def alias_sort(cursor):
    cursor.execute('SELECT * FROM Aliases')
    res = cursor.fetchall()
    cursor.execute('DELETE FROM Aliases')
    cursor.executemany("""INSERT INTO Aliases (alias, product) VALUES (?, ?)""", sorted(res, key=lambda x: (x[1], x[0])))


def library_sort(cursor):
    cursor.execute('SELECT * FROM Products')
    res = cursor.fetchall()
    cursor.execute('DELETE FROM Products')

    values = '?' + ', ?' * (len(res[0]) - 1)
    cursor.executemany(f"INSERT INTO Products VALUES ({values})", sorted(res, key=lambda x: x[0]))

def main():
    with sqlite3.connect('../../data/library.db', isolation_level=None) as connect:
        cursor = connect.cursor()

        # Сортируем
        alias_sort(cursor)
        library_sort(cursor)

        # коммитим изменения и вызываем вакум
        connect.commit()
        cursor.execute(f'VACUUM')


if __name__ == '__main__':
    main()
