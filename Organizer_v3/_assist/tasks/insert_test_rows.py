import sqlite3
from datetime import datetime, timedelta


dt_pattern = r'%Y-%m-%d %H:%M'


def create_test_task(n, d, cd, ed, ex=None):
    yield n
    yield d
    yield cd.strftime(dt_pattern)
    yield ed.strftime(dt_pattern)
    if ex is not None:
        ex = ex.strftime(dt_pattern)
    yield ex


def main():
    with sqlite3.connect('../../data/tasks.db') as connect:
        cursor = connect.cursor()

        res1 = create_test_task(
            'Просроченная задача',
            'Описание просроченной задачи',
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=1),
        )
        res2 = create_test_task(
            'Приоритетная Просроченная задача',
            'Описание просроченной задачи',
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=1, hours=10),
        )
        res3 = create_test_task(
            'Выполненная задача',
            'Описание выполненной задачи',
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=1, hours=12),
        )
        res4 = create_test_task(
            'Актуальная задача',
            None,
            datetime.now() - timedelta(hours=12),
            datetime.now() + timedelta(hours=12),
        )
        res5 = create_test_task(
            'Приоритетная Актуальная задача',
            None,
            datetime.now() - timedelta(hours=12),
            datetime.now() + timedelta(hours=2),
        )
        res6 = create_test_task(
            'Актуальная задача под выполнение',
            None,
            datetime.now(),
            datetime.now() + timedelta(days=1, hours=15),
        )

        cursor.executemany("""
            INSERT INTO Tasks (name, description, creation, end, execution)
            VALUES (?, ?, ?, ?, ?)
        """,
        (tuple(res1), tuple(res2), tuple(res3), tuple(res4), tuple(res5), tuple(res6))
        )


if __name__ == '__main__':
    main()