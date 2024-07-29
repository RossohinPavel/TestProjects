"""
Напишите скрипт на Python, который объединяет данные из двух источников. 
Первый источник - это CSV-файл с информацией о продуктах (поля: product_id, product_name). 
Второй источник - это JSON-файл с данными о продажах (поля: sale_id, product_id, amount). 
Скрипт должен объединить данные по product_id и вывести итоговую таблицу с информацией о продажах для каждого продукта.
"""
import csv
import random
import json


def create_csv_file():
    """Создает тестовый csv"""
    products = ["Pizza", "Sushi", "Tacos", "Burgers", "Fries", "Chicken Wings", "Ice Cream", "Donuts", "Steak", "Ramen"]
    with open('products.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(('product_id', 'product_name'))
        for i, product in enumerate(products, 1):
            writer.writerow((i, product))


def create_json_file():
    """Создает тестовый json"""
    sales = []
    for i in range(1, 20):
        dct = {'sale_id': i}
        dct['product_id'] = random.randint(1, 10)
        dct['amount'] = random.randint(1, 200)
        sales.append(dct)

    with open('sales.json', 'w') as file:
        json.dump(sales, file, indent=4)


def combine_csv_and_json_data():
    """Объединяет и выводит информацию из csv и json"""
    data = {'id': ['product_name', 'total']}
    with open('products.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            id, name = row
            if not id.isnumeric():
                continue
            data[int(id)] = [name, 0]

    with open('sales.json') as json_file:
        json_data = json.load(json_file)
        for row in json_data:
            product = data[row['product_id']]
            product[-1] += row['amount']

    # Немного отформатируем вывод для лучшей читаемости
    for key, values in data.items():
        name, total = values
        print(str(key).ljust(3, ' '), name.ljust(15, ' '), total)
