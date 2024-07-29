import sqlite3


def main():
    with sqlite3.connect('../../data/tasks.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""
            CREATE TABLE Tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                creation TEXT,
                end TEXT,
                execution TEXT
            )
        """)


if __name__ == '__main__':
    main()