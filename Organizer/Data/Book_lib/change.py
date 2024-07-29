import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter.ttk import Combobox

import Data.windows
import Data.Book_lib.add as add
import Data.Book_lib.operation as oper


def change(values):
    if values:
        oper.add_to_lib(values[0], values[2])
        tkmb.showinfo(title='Добавление продукта', message="Продукт отредактирован")


class change_wind(Data.windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Редактирование продуктов")
        self.child_root.geometry("500x385")
        self.to_parent_center(root)
        self.__show_static_widgets()
        self.product_widgets_frame = tk.Frame(self.child_root, width=500, height=260)
        self.product_widgets_frame.pack()
        self.focus()

    def __show_static_widgets(self):
        ask_category_lbl = tk.Label(self.child_root, text="Выберите категорию", justify=tk.LEFT)
        ask_category_lbl.pack()
        self.category_cascade = Combobox(self.child_root, state="readonly", width=30,
                                         values=self.__get_product_category())
        self.category_cascade.bind('<<ComboboxSelected>>', self.__get_product_name)
        self.category_cascade.pack()

        ask_product_lbl = tk.Label(self.child_root, text="Выберите продукт для внесения изменений", justify=tk.LEFT)
        ask_product_lbl.pack()
        self.product_cascade = Combobox(self.child_root, state="readonly", width=55)
        self.product_cascade.bind('<<ComboboxSelected>>', self.__show_product_widgets)
        self.product_cascade.pack()
        canvas = tk.Canvas(self.child_root, bg='black', width=500, height=1)
        canvas.pack()
        self.save_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                  text="Обновить значения")
        self.save_btn.place(x=2, y=355)
        exit_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                             text="Закрыть", command=self.child_root.destroy)
        exit_btn.place(x=440, y=355)

    @staticmethod
    def __get_product_category() -> list:
        # Метод возвращает список категорий для меню комбобокса
        product_category = []
        for name in oper.read_dict():
            product_category.append(name)
        return product_category

    def __get_product_name(self, event):
        # Сначала запускаем цикл для уничтожения всех "дочерних виджетов" отрисованных на основном фрейме
        for widget in self.product_widgets_frame.winfo_children():
            widget.destroy()
        # Метод - событие формирует список продуктов для комбобокса выбора продуктов
        self.product_cascade.set("")
        product_name = []
        for name in oper.read_dict()[self.category_cascade.get()]:
            product_name.append(name)
        product_name.sort()
        self.product_cascade.config(values=product_name)

    def __show_product_widgets(self, event):
        # Метод - событие отображает фреймы выбранного продукта и сохраненные значения
        # Сначала запускаем цикл для уничтожения всех "дочерних виджетов" отрисованных на основном фрейме
        for widget in self.product_widgets_frame.winfo_children():
            widget.destroy()
        # Запоминаем в переменные значение категории и продукта. Необходимо для записи
        category = self.category_cascade.get()
        product_name = self.product_cascade.get()
        product_dict = oper.read_product(category, product_name)
        match category:
            case "Фотокнига Стандарт" | "Фотокнига ЛЮКС" | "Фотокнига Классик":
                init = add.fotobook_standart(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.book_format_combo.set(product_dict['book_format'])
                init.book_option_combo.set(product_dict['book_option'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                init.cover_carton_format_combo.set(product_dict['cover_carton'])
                init.page_print_mat_combo.set(product_dict['page_material'])
                init.book_cover_canal_combo.set(product_dict['cover_canal'])
                init.book_page_canal_combo.set(product_dict['page_canal'])
                init.book_spine_value.set(product_dict['spine'])
                self.save_btn.config(command=lambda: change(init.check_value()))
            case "Фотокнига Flex Bind":
                init = add.premium_flex_bind(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.book_format_combo.set(product_dict['book_format'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                init.cover_carton_format_combo.set(product_dict['cover_carton'])
                init.page_print_mat_combo.set(product_dict['page_material'])
                init.book_spine_value.set(product_dict['spine'])
                self.save_btn.config(command=lambda: change(init.check_value()))
            case "Фотопланшет Стандарт":
                init = add.school_plan_standart(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.book_format_combo.set(product_dict['book_format'])
                init.book_option_combo.set(product_dict['book_option'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                init.cover_carton_format_combo.set(product_dict['cover_carton'])
                init.page_print_mat_combo.set(product_dict['page_material'])
                init.book_cover_canal_combo.set(product_dict['cover_canal'])
                init.book_page_canal_combo.set(product_dict['page_canal'])
                self.save_btn.config(command=lambda: change(init.check_value()))
            case "Layflat":
                init = add.layflat(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.book_format_combo.set(product_dict['book_format'])
                init.book_option_combo.set(product_dict['book_option'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                init.cover_carton_format_combo.set(product_dict['cover_carton'])
                init.page_print_mat_combo.set(product_dict['page_material'])
                init.book_spine_value.set(product_dict['spine'])
                self.save_btn.config(command=lambda: change(init.check_value()))
            case "Фотоальбом полиграфический" | "Фотоальбом PUR":
                init = add.poli_album(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.book_format_combo.set(product_dict['book_format'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                init.cover_carton_format_combo.set(product_dict['cover_carton'])
                init.page_print_mat_combo.set(product_dict['page_material'])
                init.book_spine_value.set(product_dict['spine'])
                self.save_btn.config(command=lambda: change(init.check_value()))
            case "Фотожурнал":
                init = add.poli_jur(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.book_format_combo.set(product_dict['book_format'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                init.page_print_mat_combo.set(product_dict['page_material'])
                self.save_btn.config(command=lambda: change(init.check_value()))
            case "Фотопапка":
                init = add.foto_pap(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.book_format_combo.set(product_dict['book_format'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                init.cover_carton_format_combo.set(product_dict['cover_carton'])
                init.page_print_mat_combo.set(product_dict['page_material'])
                self.save_btn.config(command=lambda: change(init.check_value()))
            case "Фотопечать SRA" | "Фотопечать" | "Субпродукты":
                init = add.poli_print(self.product_widgets_frame, category)
                init.full_name_value.set(product_name)
                init.full_name_entry.config(state="readonly")
                init.short_name_combo.set(product_dict['short_name'])
                init.cover_print_mat_combo.set(product_dict['cover_material'])
                self.save_btn.config(command=lambda: change(init.check_value()))
