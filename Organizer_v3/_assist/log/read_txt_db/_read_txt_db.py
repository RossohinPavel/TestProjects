import sqlite3
import pickle
import os


MEM = {}

if not os.path.exists('db.mem'):
    with open('db.mem', 'wb') as file:
        pickle.dump(MEM, file)

with open('db.mem', 'rb') as file:
    MEM.update(pickle.load(file))


txts = tuple(x for x in os.listdir() if x.startswith('OR') and x.endswith('.txt'))

for txt in txts:
    with open(txt, 'r', encoding='utf-8') as file:
        file.readline()
        for line in file.readlines()[1:]:
            lst = line.strip().split('\t')
            if len(lst) == 7:
                MEM[lst[0]] = (lst[3], lst[-3], float(lst[-1].replace(',', '.')))


with open('db.mem', 'wb') as file:
    pickle.dump(MEM, file)
