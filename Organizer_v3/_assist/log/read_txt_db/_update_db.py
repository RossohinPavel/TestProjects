import pickle
import sqlite3


with open('db.mem', 'rb') as file:
    MEM = pickle.load(file)


with sqlite3.connect('../../../data/log.db') as connect:
    cursor = connect.cursor()
    for k, v in MEM.items():
        cursor.execute(f'SELECT * FROM Orders WHERE name={k}')
        if not cursor.fetchone():
            continue
        print(k)
        cursor.execute(f'UPDATE Orders SET customer_name=\'{v[0]}\', customer_address=\'{v[1]}\', price={v[2]} WHERE name=\'{k}\'')
        connect.commit()
        
