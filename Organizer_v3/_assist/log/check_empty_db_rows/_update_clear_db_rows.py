import pickle
import sqlite3
from os.path import exists as p_exists


MEM = {}


def get_solutions(line):
    if line[1] not in MEM:
        print('-'*100)
        print(line)
        sol = input('Вы хотите обновить данные для этого заказа (д/н/в)?')
        if sol == 'д':
            return sol
        if sol == 'н':
            MEM[line[1]] = sol
            with open('solutions.mem', 'wb') as file:
                pickle.dump(MEM, file)
        else:
            raise Exception('Выход из программы')
    return MEM[line[1]]


def get_new_data(line):
    print(f"Введите новое имя вместо <{line[-3]}>")
    customer_name = input()
    print(f"Введите новый адрес вместо <{line[-2]}>")
    customer_address = input()
    print(f"Введите новую сумму вместо <{line[-1]}>")
    price = float(input())
    return *line[:3], customer_name, customer_address, price


if p_exists('solutions.mem'):
    with open('solutions.mem', 'rb') as file:
        MEM.update(pickle.load(file))
else:
    with open('solutions.mem', 'wb') as file:
        pickle.dump(MEM, file)


with sqlite3.connect('../../../data/log.db') as connect:
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM Orders WHERE customer_name="Unknown" OR customer_name="Диспетчер ФотокнигиОптом" OR customer_name="РОЗНИЦА КОЛИЗЕЙ" OR price=0.0')
    for line in reversed(cursor.fetchall()):
        if get_solutions(line) == 'д':
            new_line = get_new_data(line)
            cursor.execute(f'UPDATE Orders SET customer_name=\'{new_line[-3]}\', customer_address=\'{new_line[-2]}\', price={new_line[-1]} WHERE name=\'{line[1]}\'')
            connect.commit()
