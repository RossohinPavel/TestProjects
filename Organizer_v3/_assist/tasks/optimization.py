import sqlite3


def main():
    with sqlite3.connect('../../data/tasks.db') as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT id FROM Tasks')
        res = cursor.fetchall()

        step = 1

        while res:
            row = res.pop(0)[0]
            cursor.execute('UPDATE Tasks SET id=? WHERE id=?', (step, row))
            step += 1
        
        cursor.execute('UPDATE sqlite_sequence SET seq=? WHERE name=?', (step - 1, 'Tasks'))
        connect.commit()
        cursor.execute(f'VACUUM')


if __name__ == '__main__':
    main()
