"""Оптимизация и сортировка базы данных текстовых шаблонов"""


import sqlite3


def mail_samples_sort(cursor):
    cursor.execute('SELECT * FROM Samples')
    res = cursor.fetchall()
    cursor.execute('DELETE FROM Samples')
    cursor.executemany(
        "INSERT INTO Samples (name, tag, data) VALUES (?, ?, ?)", 
        sorted(res, key=lambda x: (x[1], x[0]))
    )


def main():
    with sqlite3.connect('../../data/mail_samples.db', isolation_level=None) as connect:
        cursor = connect.cursor()

        # Сортируем
        mail_samples_sort(cursor)

        # коммитим изменения и вызываем вакум
        connect.commit()
        cursor.execute(f'VACUUM')


if __name__ == '__main__':
    main()
