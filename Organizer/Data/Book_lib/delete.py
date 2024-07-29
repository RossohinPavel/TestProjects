import json
import tkinter as tk
from tkinter import messagebox as tkmb
from tkinter.ttk import Combobox

import Data.windows


class delete_wind(Data.windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Удаление продукта")
        self.child_root.geometry("300x130")
        self.to_parent_center(root)
        self.__show_widgets()
        self.focus()

    def __show_widgets(self):
        ask_category_lbl = tk.Label(self.child_root, justify=tk.LEFT, text="Выберете категорию")
        ask_category_lbl.pack()
        self.category_cascade = Combobox(self.child_root, state="readonly", width=36,
                                         values=self.__get_product_category())
        self.category_cascade.bind('<<ComboboxSelected>>', self.__get_category_to_show_product)
        self.category_cascade.pack()

        ask_product_lbl = tk.Label(self.child_root, text="Выбирите продукт для удаления из библиотеки")
        ask_product_lbl.pack()
        self.product_cascade = Combobox(self.child_root, state="readonly", width=45)
        self.product_cascade.pack()

        delete_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                               text="Удалить", command=self.__delete_product)
        delete_btn.pack(side=tk.LEFT, padx=4)
        exit_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                             text="Сохранить и выйти", command=self.child_root.destroy)
        exit_btn.pack(side=tk.RIGHT, padx=4)

    @staticmethod
    def __get_product_category() -> list:
        # Метод возвращает список категорий для меню комбобокса
        product_category = []
        with open("Data\\Settings\\book_lib.json", "r") as file:
            book_lib = json.load(file)
        for name in book_lib:
            product_category.append(name)
        return product_category

    def __get_category_to_show_product(self, event=None):
        # Метод - событие обновляет список продуктов для выбранной категории в комбобоксе
        product_name_list = []
        with open("Data\\Settings\\book_lib.json", "r") as file:
            book_lib = json.load(file)
        for name in book_lib[self.category_cascade.get()]:
            product_name_list.append(name)
        product_name_list.sort()
        self.product_cascade.config(values=product_name_list)

    def __delete_product(self):
        # Метод удаляет продут исходя из выбранных значений
        category = self.category_cascade.get()
        product = self.product_cascade.get()
        if category and product:
            with open("Data\\Settings\\book_lib.json", "r") as file:
                book_lib = json.load(file)
            del book_lib[category][product]
            with open("Data\\Settings\\book_lib.json", "w") as file:
                json.dump(book_lib, file, indent=4)
            self.product_cascade.set("")
            self.__get_category_to_show_product()
            tkmb.showinfo(title="Удаление продукта", message="Продукт удален")
