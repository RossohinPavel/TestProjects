import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter.ttk import Combobox

import Data.windows
import Data.Book_lib.mat_list as ml
import Data.Book_lib.operation as oper


def add(values):
    # Проверка на наличие добавляемого продукта. Values[0] - категория, [1] - полное имя продукта. [2] - словарь прдукта
    if values:
        if values[1] in oper.read_dict()[values[0]]:
            tkmb.showwarning(title="Проверка", message="Добавляемый продукт уже есть в библиотеке")
        else:
            oper.add_to_lib(values[0], values[2])
            tkmb.showinfo(title='Добавление продукта', message="Продукт успешно добавлен")


class add_wind(Data.windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Добавление продукта")
        self.child_root.geometry("500x345")
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
        self.category_cascade.bind('<<ComboboxSelected>>', self.__get_category_to_show_product)
        self.category_cascade.pack()
        canvas = tk.Canvas(self.child_root, bg='black', width=500, height=1)
        canvas.pack()
        self.save_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                  text="Сохранить в библиотеку")
        self.save_btn.place(x=2, y=310)
        exit_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                             text="Закрыть", command=self.child_root.destroy)
        exit_btn.place(x=440, y=310)

    @staticmethod
    def __get_product_category() -> list:
        # Метод возвращает список категорий для меню комбобокса
        product_category = []
        for name in oper.read_dict():
            product_category.append(name)
        return product_category

    def __get_category_to_show_product(self, event):
        # Метод - событие отображает фреймы с продуктами в зависимости от выбранной категории
        # Сначала запускаем цикл для уничтожения всех "дочерних виджетов" отрисованных на основном фрейме
        for widget in self.product_widgets_frame.winfo_children():
            widget.destroy()
        # Запоминаем в переменную значение категории. Необходимо для выбора и записи
        category = self.category_cascade.get()
        match category:
            case "Фотокнига Стандарт" | "Фотокнига ЛЮКС" | "Фотокнига Классик":
                init = fotobook_standart(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))
            case "Фотокнига Flex Bind":
                init = premium_flex_bind(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))
            case "Фотопланшет Стандарт":
                init = school_plan_standart(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))
            case "Layflat":
                init = layflat(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))
            case "Фотоальбом полиграфический" | "Фотоальбом PUR":
                init = poli_album(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))
            case "Фотожурнал":
                init = poli_jur(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))
            case "Фотопапка":
                init = foto_pap(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))
            case "Фотопечать SRA" | "Фотопечать" | "Субпродукты":
                init = poli_print(self.product_widgets_frame, category)
                self.save_btn.config(command=lambda: add(init.check_value(clear_widget=True)))


class fotobook_standart:  # Эта категория подходит под книги премиум стандарт, премиум люкс, выпускная классик
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.book_spine_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)
        self.__show_print_conf_widget(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)
        book_format_lbl = tk.Label(root, text="Выберите формат книги")
        book_format_lbl.place(x=2, y=82)
        self.book_format_combo = Combobox(root, width=36, values=ml.sorted_list(ml.print_format_list), state="readonly")
        self.book_format_combo.place(x=5, y=102)
        book_option_lbl = tk.Label(root, text="Выберите опции сборки книги")
        book_option_lbl.place(x=2, y=123)
        self.book_option_combo = Combobox(root, width=36, state="readonly", values=ml.book_option_list)
        self.book_option_combo.place(x=5, y=143)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)
        cover_carton_format_lbl = tk.Label(root, text="Выберите картонку для обложки")
        cover_carton_format_lbl.place(x=250, y=41)
        self.cover_carton_format_combo = Combobox(root, width=36, state="readonly",
                                                  values=ml.sorted_list(ml.cover_carton_list))
        self.cover_carton_format_combo.place(x=253, y=61)
        page_print_mat_lbl = tk.Label(root, text="Выберите печатный материал разворотов")
        page_print_mat_lbl.place(x=250, y=82)
        self.page_print_mat_combo = Combobox(root, width=36, state="readonly",
                                             values=ml.sorted_list(ml.print_mat_list))
        self.page_print_mat_combo.place(x=253, y=102)

    def __show_print_conf_widget(self, root):
        print_canvas = tk.Canvas(root, bg='black', width=491, height=1)
        print_canvas.place(x=2, y=170)
        book_cover_canal_lbl = tk.Label(root, text="Выберите 'канал' для обложки")
        book_cover_canal_lbl.place(x=2, y=175)
        self.book_cover_canal_combo = Combobox(root, width=36, values=ml.sorted_list(ml.canal_list), state="readonly")
        self.book_cover_canal_combo.place(x=5, y=195)
        book_page_canal_lbl = tk.Label(root, text="Выберите 'канал' для разворотов")
        book_page_canal_lbl.place(x=250, y=175)
        self.book_page_canal_combo = Combobox(root, width=36, values=ml.sorted_list(ml.canal_list), state="readonly")
        self.book_page_canal_combo.place(x=253, y=195)
        books_spine_lbl = tk.Label(root, text="Введите значение в пикселях для отрисовки направляющих", justify=tk.LEFT)
        books_spine_lbl.place(x=2, y=216)
        books_spine_entry = tk.Entry(root, textvariable=self.book_spine_value, width=39)
        books_spine_entry.place(x=5, y=236)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo, self.book_format_combo, self.book_option_combo,
                       self.cover_print_mat_combo, self.cover_carton_format_combo, self.page_print_mat_combo,
                       self.book_cover_canal_combo, self.book_page_canal_combo, self.book_spine_value]
        check_value = 0
        lam = "гля"
        if self.category == "Фотокнига ЛЮКС":
            lam = "мат"
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "book_format": self.book_format_combo.get(),
                "book_option": self.book_option_combo.get(),
                "cover_material": self.cover_print_mat_combo.get(),
                "cover_carton": self.cover_carton_format_combo.get(),
                "page_material": self.page_print_mat_combo.get(),
                "cover_canal": self.book_cover_canal_combo.get(),
                "page_canal": self.book_page_canal_combo.get(),
                "spine": self.book_spine_value.get(),
                "lamination": lam}
            }
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")


class premium_flex_bind:
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.book_spine_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)
        self.__show_print_conf_widget(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)
        book_format_lbl = tk.Label(root, text="Выберите формат книги")
        book_format_lbl.place(x=2, y=82)
        self.book_format_combo = Combobox(root, width=36, values=ml.sorted_list(ml.print_format_list), state="readonly")
        self.book_format_combo.place(x=5, y=102)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)
        cover_carton_format_lbl = tk.Label(root, text="Выберите картонку для обложки")
        cover_carton_format_lbl.place(x=250, y=41)
        self.cover_carton_format_combo = Combobox(root, width=36, state="readonly",
                                                  values=ml.sorted_list(ml.cover_carton_list))
        self.cover_carton_format_combo.place(x=253, y=61)
        page_print_mat_lbl = tk.Label(root, text="Выберите печатный материал разворотов")
        page_print_mat_lbl.place(x=250, y=82)
        self.page_print_mat_combo = Combobox(root, width=36, state="readonly", values=ml.sorted_list(ml.print_mat_list))
        self.page_print_mat_combo.place(x=253, y=102)

    def __show_print_conf_widget(self, root):
        print_canvas = tk.Canvas(root, bg='black', width=491, height=1)
        print_canvas.place(x=2, y=170)
        books_spine_lbl = tk.Label(root, text="Введите значение в пикселях для отрисовки направляющих", justify=tk.LEFT)
        books_spine_lbl.place(x=2, y=216)
        books_spine_entry = tk.Entry(root, textvariable=self.book_spine_value, width=39)
        books_spine_entry.place(x=5, y=236)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo, self.book_format_combo, self.cover_print_mat_combo,
                       self.cover_carton_format_combo, self.page_print_mat_combo, self.book_spine_value]
        check_value = 0
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "book_format": self.book_format_combo.get(),
                "cover_material": self.cover_print_mat_combo.get(),
                "cover_carton": self.cover_carton_format_combo.get(),
                "page_material": self.page_print_mat_combo.get(),
                "spine": self.book_spine_value.get(),
                "lamination": "мат"}
            }
            # Проверка на наличие добавляемого продукта в библиотеке
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")


class school_plan_standart:
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)
        self.__show_print_conf_widget(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)
        book_format_lbl = tk.Label(root, text="Выберите формат книги")
        book_format_lbl.place(x=2, y=82)
        self.book_format_combo = Combobox(root, width=36, values=ml.sorted_list(ml.print_format_list), state="readonly")
        self.book_format_combo.place(x=5, y=102)
        book_option_lbl = tk.Label(root, text="Выберите опции сборки книги")
        book_option_lbl.place(x=2, y=123)
        self.book_option_combo = Combobox(root, width=36, state="readonly", values=ml.book_option_list)
        self.book_option_combo.place(x=5, y=143)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)
        cover_carton_format_lbl = tk.Label(root, text="Выберите картонку для обложки")
        cover_carton_format_lbl.place(x=250, y=41)
        self.cover_carton_format_combo = Combobox(root, width=36, state="readonly",
                                                  values=ml.sorted_list(ml.cover_carton_list))
        self.cover_carton_format_combo.place(x=253, y=61)
        page_print_mat_lbl = tk.Label(root, text="Выберите печатный материал разворотов")
        page_print_mat_lbl.place(x=250, y=82)
        self.page_print_mat_combo = Combobox(root, width=36, state="readonly",
                                             values=ml.sorted_list(ml.print_mat_list))
        self.page_print_mat_combo.place(x=253, y=102)

    def __show_print_conf_widget(self, root):
        print_canvas = tk.Canvas(root, bg='black', width=491, height=1)
        print_canvas.place(x=2, y=170)
        book_cover_canal_lbl = tk.Label(root, text="Выберите 'канал' для обложки")
        book_cover_canal_lbl.place(x=2, y=175)
        self.book_cover_canal_combo = Combobox(root, width=36, values=ml.sorted_list(ml.canal_list), state="readonly")
        self.book_cover_canal_combo.place(x=5, y=195)
        book_page_canal_lbl = tk.Label(root, text="Выберите 'канал' для разворотов")
        book_page_canal_lbl.place(x=250, y=175)
        self.book_page_canal_combo = Combobox(root, width=36, values=ml.sorted_list(ml.canal_list), state="readonly")
        self.book_page_canal_combo.place(x=253, y=195)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo, self.book_format_combo, self.book_option_combo,
                       self.cover_print_mat_combo, self.cover_carton_format_combo, self.page_print_mat_combo,
                       self.book_cover_canal_combo, self.book_page_canal_combo]
        check_value = 0
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "book_format": self.book_format_combo.get(),
                "book_option": self.book_option_combo.get(),
                "cover_material": self.cover_print_mat_combo.get(),
                "cover_carton": self.cover_carton_format_combo.get(),
                "page_material": self.page_print_mat_combo.get(),
                "cover_canal": self.book_cover_canal_combo.get(),
                "page_canal": self.book_page_canal_combo.get(),
                "lamination": "гля"}
            }
            # Проверка на наличие добавляемого продукта в библиотеке
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")


class layflat:
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.book_spine_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)
        self.__show_print_conf_widget(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)
        book_format_lbl = tk.Label(root, text="Выберите формат книги")
        book_format_lbl.place(x=2, y=82)
        self.book_format_combo = Combobox(root, width=36, values=ml.sorted_list(ml.print_format_list), state="readonly")
        self.book_format_combo.place(x=5, y=102)
        book_option_lbl = tk.Label(root, text="Выберите опции сборки книги")
        book_option_lbl.place(x=2, y=123)
        self.book_option_combo = Combobox(root, width=36, state="readonly", values=ml.book_option_list)
        self.book_option_combo.place(x=5, y=143)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)
        cover_carton_format_lbl = tk.Label(root, text="Выберите картонку для обложки")
        cover_carton_format_lbl.place(x=250, y=41)
        self.cover_carton_format_combo = Combobox(root, width=36, state="readonly",
                                                  values=ml.sorted_list(ml.cover_carton_list))
        self.cover_carton_format_combo.place(x=253, y=61)
        page_print_mat_lbl = tk.Label(root, text="Выберите печатный материал разворотов")
        page_print_mat_lbl.place(x=250, y=82)
        self.page_print_mat_combo = Combobox(root, width=36, state="readonly",
                                             values=ml.sorted_list(ml.print_mat_list))
        self.page_print_mat_combo.place(x=253, y=102)

    def __show_print_conf_widget(self, root):
        print_canvas = tk.Canvas(root, bg='black', width=491, height=1)
        print_canvas.place(x=2, y=170)
        books_spine_lbl = tk.Label(root, text="Введите значение в пикселях для отрисовки направляющих", justify=tk.LEFT)
        books_spine_lbl.place(x=2, y=216)
        books_spine_entry = tk.Entry(root, textvariable=self.book_spine_value, width=39)
        books_spine_entry.place(x=5, y=236)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo, self.book_format_combo, self.book_option_combo,
                       self.cover_print_mat_combo, self.cover_carton_format_combo, self.page_print_mat_combo,
                       self.book_spine_value]
        check_value = 0
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "book_format": self.book_format_combo.get(),
                "book_option": self.book_option_combo.get(),
                "cover_material": self.cover_print_mat_combo.get(),
                "cover_carton": self.cover_carton_format_combo.get(),
                "page_material": self.page_print_mat_combo.get(),
                "spine": self.book_spine_value.get(),
                "lamination": "гля"}

            }
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")


class poli_album:
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.book_spine_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)
        self.__show_print_conf_widget(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)
        book_format_lbl = tk.Label(root, text="Выберите формат книги")
        book_format_lbl.place(x=2, y=82)
        self.book_format_combo = Combobox(root, width=36, values=ml.sorted_list(ml.print_format_list), state="readonly")
        self.book_format_combo.place(x=5, y=102)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)
        cover_carton_format_lbl = tk.Label(root, text="Выберите картонку для обложки")
        cover_carton_format_lbl.place(x=250, y=41)
        self.cover_carton_format_combo = Combobox(root, width=36, state="readonly",
                                                  values=ml.sorted_list(ml.cover_carton_list))
        self.cover_carton_format_combo.place(x=253, y=61)
        page_print_mat_lbl = tk.Label(root, text="Выберите печатный материал разворотов")
        page_print_mat_lbl.place(x=250, y=82)
        self.page_print_mat_combo = Combobox(root, width=36, state="readonly",
                                             values=ml.sorted_list(ml.print_mat_list))
        self.page_print_mat_combo.place(x=253, y=102)

    def __show_print_conf_widget(self, root):
        print_canvas = tk.Canvas(root, bg='black', width=491, height=1)
        print_canvas.place(x=2, y=170)
        books_spine_lbl = tk.Label(root, text="Введите значение в пикселях для отрисовки направляющих", justify=tk.LEFT)
        books_spine_lbl.place(x=2, y=216)
        books_spine_entry = tk.Entry(root, textvariable=self.book_spine_value, width=39)
        books_spine_entry.place(x=5, y=236)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo, self.book_format_combo, self.cover_print_mat_combo,
                       self.cover_carton_format_combo, self.page_print_mat_combo, self.book_spine_value]
        check_value = 0
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "book_format": self.book_format_combo.get(),
                "cover_material": self.cover_print_mat_combo.get(),
                "cover_carton": self.cover_carton_format_combo.get(),
                "page_material": self.page_print_mat_combo.get(),
                "spine": self.book_spine_value.get(),
                "lamination": "гля"}
            }
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")


class poli_jur:
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)
        book_format_lbl = tk.Label(root, text="Выберите формат книги")
        book_format_lbl.place(x=2, y=82)
        self.book_format_combo = Combobox(root, width=36, values=ml.sorted_list(ml.print_format_list), state="readonly")
        self.book_format_combo.place(x=5, y=102)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)
        page_print_mat_lbl = tk.Label(root, text="Выберите печатный материал разворотов")
        page_print_mat_lbl.place(x=250, y=82)
        self.page_print_mat_combo = Combobox(root, width=36, state="readonly",
                                             values=ml.sorted_list(ml.print_mat_list))
        self.page_print_mat_combo.place(x=253, y=102)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo, self.book_format_combo, self.cover_print_mat_combo,
                       self.page_print_mat_combo]
        check_value = 0
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "book_format": self.book_format_combo.get(),
                "cover_material": self.cover_print_mat_combo.get(),
                "page_material": self.page_print_mat_combo.get()}
            }
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")


class foto_pap:
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)
        book_format_lbl = tk.Label(root, text="Выберите формат книги")
        book_format_lbl.place(x=2, y=82)
        self.book_format_combo = Combobox(root, width=36, values=ml.sorted_list(ml.print_format_list), state="readonly")
        self.book_format_combo.place(x=5, y=102)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)
        cover_carton_format_lbl = tk.Label(root, text="Выберите картонку для обложки")
        cover_carton_format_lbl.place(x=250, y=41)
        self.cover_carton_format_combo = Combobox(root, width=36, state="readonly",
                                                  values=ml.sorted_list(ml.cover_carton_list))
        self.cover_carton_format_combo.place(x=253, y=61)
        page_print_mat_lbl = tk.Label(root, text="Выберите печатный материал разворотов")
        page_print_mat_lbl.place(x=250, y=82)
        self.page_print_mat_combo = Combobox(root, width=36, state="readonly",
                                             values=ml.sorted_list(ml.print_mat_list))
        self.page_print_mat_combo.place(x=253, y=102)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo, self.book_format_combo, self.cover_print_mat_combo,
                       self.cover_carton_format_combo, self.page_print_mat_combo]
        check_value = 0
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "book_format": self.book_format_combo.get(),
                "cover_material": self.cover_print_mat_combo.get(),
                "cover_carton": self.cover_carton_format_combo.get(),
                "page_material": self.page_print_mat_combo.get(),
                "lamination": "гля"}
            }
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")


class poli_print:     # Класс используется для всего остального
    def __init__(self, root, category):
        # Переменные для сохранения значений выбранных в виджетах
        self.category = category
        self.full_name_value = tk.StringVar(root)
        self.__show_widget_left_column(root)
        self.__show_widget_right_column(root)

    def __show_widget_left_column(self, root):
        full_name_lbl = tk.Label(root, text="Введите полное имя продукта")
        full_name_lbl.place(x=2, y=0)
        self.full_name_entry = tk.Entry(root, textvariable=self.full_name_value, width=39)
        self.full_name_entry.place(x=5, y=21)
        short_name_lbl = tk.Label(root, text="Выберите короткое имя")
        short_name_lbl.place(x=2, y=41)
        self.short_name_combo = Combobox(root, width=36, values=ml.short_name_list, state="readonly")
        self.short_name_combo.place(x=5, y=61)

    def __show_widget_right_column(self, root):
        cover_print_mat_lbl = tk.Label(root, text="Выберите печатный материал обложки")
        cover_print_mat_lbl.place(x=250, y=0)
        self.cover_print_mat_combo = Combobox(root, width=36, state="readonly",
                                              values=ml.sorted_list(ml.print_mat_list))
        self.cover_print_mat_combo.place(x=253, y=20)

    def check_value(self, clear_widget=False):
        # Получаем значения всех переменных для проверки на присутствие значений
        check_tuple = [self.full_name_value, self.short_name_combo]
        check_value = 0
        for value in check_tuple:
            if value.get():
                check_value += 1
        if len(check_tuple) == check_value:
            name = self.full_name_value.get()
            product_dict = {name: {
                "short_name": self.short_name_combo.get(),
                "cover_material": self.cover_print_mat_combo.get()}
            }
            if clear_widget:
                for value in check_tuple:
                    value.set("")
            return self.category, name, product_dict
        else:
            tkmb.showwarning(title="Проверка", message="Введены не все значения")
