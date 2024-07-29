import sqlite3


def create_clear_app_db():
    with sqlite3.connect('../../data/settings.db') as connect:
        cursor = connect.cursor()
        cursor.execute('CREATE TABLE Settings (name PRIMARY KEY, data INT)')


def fill_settings_table():
    with sqlite3.connect('../../data/settings.db') as connect:
        cursor = connect.cursor()
        values = (
            ('autolog', 0), 
            ('log_check_depth', 30), 
            ('z_disc', '/mnt/HDD/Tests/Book'), 
            ('o_disc', '/mnt/HDD/_Dest'), 
            ('t_disc', '/mnt/HDD/_Dest'), 
            ('roddom_dir', '/mnt/HDD/Tests/Роддом'),
            ('theme', 'light'),
            ('color', 'flatly')
            )
        cursor.executemany('INSERT INTO Settings (name, data) VALUES (?, ?)', values)
        connect.commit()


if __name__ == '__main__':
    create_clear_app_db()
    fill_settings_table()
    pass