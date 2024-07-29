import json


def add_to_lib(class_type, value):
    # Метод используется для записи (обновления или добавления) продукта в библиотеку
    with open("Data/Settings/book_lib.json", "r") as file:
        book_lib = json.load(file)
    book_lib[class_type].update(value)
    with open("Data/Settings/book_lib.json", "w") as file:
        json.dump(book_lib, file, indent=4, ensure_ascii=False)


def read_dict() -> dict:
    # Метод возвращает словарь в режиме чтения из библиотеки
    with open("Data/Settings/book_lib.json", "r") as file:
        book_lib = json.load(file)
    return book_lib


def read_product(category, product_name) -> dict:
    with open("Data/Settings/book_lib.json", "r") as file:
        book_lib = json.load(file)
    return book_lib[category][product_name]
