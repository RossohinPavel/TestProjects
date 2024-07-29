import sqlite3
import new_modules.Lib.ProductCreator as PC


obj_list = tuple(PC.__dict__[product]() for product in PC.__all__)


with sqlite3.connect('../data/library.db') as lib:
    cursor = lib.cursor()
    for obj in obj_list:
        descr = ',\n'.join(f'{k} {v}' for k, v in obj.get_descr_to_sqldb().items())
        sql_req = f'CREATE TABLE {obj.__class__.category}\n(id INTEGER PRIMARY KEY AUTOINCREMENT,\n{descr})'
        cursor.execute(sql_req)
        keys = []
        values = []
        for key, value in obj.__dict__.items():
            if key == 'full_name':
                value = f'{obj.category}_test'
            if type(value) is list:
                value = value[0]
            keys.append(f'\"{key}\"')
            values.append(f'\"{value}\"')
        keys = ', '.join(keys)
        values = ', '.join(values)
        req = f'INSERT INTO {obj.category} ({keys}) VALUES ({values})'
        cursor.execute(req)
        lib.commit()
