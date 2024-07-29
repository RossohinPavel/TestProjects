"""
    Образец sql запросов на работу с псевдонимами в базе данных
"""


import sqlite3 


def delete(aliases):
    req = ', '.join(repr(x) for x in aliases)
    cursor.execute(
        f"""DELETE FROM Aliases WHERE alias IN ({req}) AND category=? AND product_id=?""",
        (category, id)
    )

def add(aliases):
    cursor.executemany(
        'INSERT INTO Aliases (alias, category, product_id) VALUES (?, ?, ?)', 
        ((x, category, id) for x in aliases)
    )
   


with sqlite3.connect('../data/library.db') as connect:
    cursor = connect.cursor()

    category, id = 'Album', 1

    # Добавление тестовых псевдонимов
    cursor.execute('INSERT INTO Aliases (alias, category, product_id) VALUES (?, ?, ?)', ('test', category, id))
    cursor.execute('INSERT INTO Aliases (alias, category, product_id) VALUES (?, ?, ?)', ('test1', category, id))
    cursor.execute('INSERT INTO Aliases (alias, category, product_id) VALUES (?, ?, ?)', ('test2', category, id))
    cursor.execute('SELECT * FROM Aliases')
    print('--- NEW ---\n', cursor.fetchall())

    cursor.execute(
        """SELECT alias FROM Aliases WHERE category=? AND product_id=?""",
        (category, id)
    )
    res = set(x[0] for x in cursor.fetchall())

    eq = set(('test1', 'test2', 'test4'))

    to_del, to_add = res - eq, eq - res

    print('to_del', to_del)
    print('to_add', to_add)

    if to_del: delete(to_del)
    if to_add: add(to_add)

    cursor.execute('SELECT * FROM Aliases')
    print('--- END ---\n', cursor.fetchall())    

    cursor.execute('DELETE FROM Aliases')