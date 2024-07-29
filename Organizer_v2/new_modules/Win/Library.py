import new_modules.Win.Source as Source
from new_modules.Lib.Library import Library


class LibraryWindow(Source.ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Библиотека')
        self.tree = None
        self.lib = Library()
        self.show_main_widget()
        self.resizable(False, False)
        self.set_treeview_values()
        self.to_parent_center()
        self.focus()

    def show_main_widget(self):
        """Отрисовка виджетов основного меню библиотеки"""
        x_leveler = Source.tk.Frame(self, width=300)    # Выравнивание тривью по текущему значению
        x_leveler.grid(row=0, column=0)
        self.tree = Source.ttk.Treeview(self, show='tree', height=15)
        self.tree.grid(row=1, column=0, padx=2, pady=2, sticky=Source.tk.NSEW, rowspan=5)
        x_scroll = Source.ttk.Scrollbar(self, orient=Source.tk.HORIZONTAL, command=self.tree.xview)
        self.tree.config(xscroll=x_scroll.set)
        x_scroll.grid(row=6, column=0, sticky=Source.tk.EW)
        y_scroll = Source.ttk.Scrollbar(self, orient=Source.tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscroll=y_scroll.set)
        y_scroll.grid(row=1, column=1, sticky=Source.tk.NS, rowspan=5)
        add_btn = Source.MyButton(self, text='Добавить', command=self.add_to_lib)
        add_btn.grid(row=1, column=2, sticky=Source.tk.EW, padx=2, pady=2)
        copy_btn = Source.MyButton(self, text='Копировать', command=self.copy_from_lib)
        copy_btn.grid(row=2, column=2, sticky=Source.tk.EW, padx=2, pady=2)
        change_btn = Source.MyButton(self, text='Изменить', command=self.change_lib)
        change_btn.grid(row=3, column=2, sticky=Source.tk.EW, padx=2, pady=2)
        del_btn = Source.MyButton(self, text='Удалить', command=self.delete_from_lib)
        del_btn.grid(row=4, column=2, sticky=Source.tk.EW, padx=2, pady=2)
        y_leveler = Source.tk.Frame(self, height=200)
        y_leveler.grid(row=5, column=2)
        close_btn = Source.MyButton(self, text='Закрыть', command=self.destroy)
        close_btn.grid(row=6, column=2, sticky=Source.tk.EW, rowspan=2, padx=2, pady=2)

    def set_treeview_values(self):
        """Метод для установки значений в тривью"""
        key_index = 1
        for key, values in self.lib.get_product_names().items():
            self.tree.insert('', Source.tk.END, iid=key_index, text=self.lib.translator(key))
            for index, value in enumerate(values):
                self.tree.insert(key_index, Source.tk.END, iid=int(f'{key_index}{index}'), text=value, tags=key)
            key_index += 1

    def get_treeview_values(self) -> tuple | None:
        """Метод для получения данных из виджета. Возвращает кортеж (название таблицы в бд, имя)"""
        index = self.tree.selection()
        if not index or len(index[0]) == 1:
            return
        item = self.tree.item(index[0])
        return item['tags'][0], item['text']

    def clear_treeview(self):
        """Очитска тривью от содержимого"""
        for i in self.tree.get_children(''):
            self.tree.delete(i)

    def add_to_lib(self):
        AddToLibWindow(self)
        self.clear_treeview()
        self.set_treeview_values()
        self.focus()

    def copy_from_lib(self):
        product = self.get_treeview_values()
        if product:
            CopyFromLibWindow(self, product)
            self.clear_treeview()
            self.set_treeview_values()
        self.focus()

    def change_lib(self):
        product = self.get_treeview_values()
        if product:
            ChangeLibWindow(self, product)
        self.focus()

    def delete_from_lib(self):
        """Удаление продукта по выбору в тривью из библиотеки"""
        values = self.get_treeview_values()
        if not values:
            return
        self.lib.delete(*values)
        self.clear_treeview()
        self.set_treeview_values()
        Source.tkmb.showinfo(title="Удаление продукта", message=f'{values[1]}\nУспешно удален из библиотеки')


class AssistWindow(Source.ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    __FRAMES = {'full_name': ('entry', 'Введите полное имя продукта', 4, 0, 81),
                'segment': ('radio', 'Выберите сегмент продукции', 4, 41),
                'short_name': ('combo', 'Выберите короткое имя', 4, 82),
                'product_format': ('combo', 'Выберите формат книги', 4, 123),
                'book_option': ('radio', 'Выберите опции сборки книги', 4, 164),
                'lamination': ('radio', 'Выберите ламинацию для продукта', 4, 205),
                'cover_print_mat': ('combo', 'Выберите печатный материал обложки', 256, 41),
                'cover_carton': ('combo', 'Выберите картонку для обложки', 256, 82),
                'page_print_mat': ('combo', 'Выберите печатный материал разворотов', 256, 123),
                'dc_break': ('check', 'Раскодировка с разрывом', 270, 221),
                'cover_type': ('radio', 'Выберите тип обложки', 256, 164),
                'gl_pos': ('entry', "Введите позицию направляющих", 4, 251),
                'gl_len': ('entry', 'Введите длинну направляющих в мм', 4, 292),
                'cover_canal': ('combo', "Выберите 'канал' обложки", 256, 251),
                'page_canal': ('combo', "Выберите 'канал' разворотов", 256, 292),
                'dc_overlap': ('entry', 'НАХЛЕСТ для переплета в мм', 256, 251),
                'dc_top_indent': ('entry', 'Введите значение отступа СВЕРХУ в мм', 256, 292),
                'dc_left_indent': ('entry', 'Введите значение отступа СЛЕВА в мм', 256, 333)
                }

    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.lib = Library()    # Ссылка на объект библиотеки
        self.product_obj = None     # Переменная для хранения объекта продукта из конструктора
        self.product_menus_frame = Source.tk.Frame(self, width=500, height=380)     # Контейнер для основных виджетов
        self.resizable(False, False)

    def product_menus_frame_clearing(self):
        """Очистка меню-виджета от ненужных фреймов"""
        for widget in self.product_menus_frame.winfo_children():
            widget.destroy()

    def show_buttons(self, text, command):
        """Функция для отрисовки кнопок"""
        frame = Source.tk.Frame(self, width=500, height=30)
        func_button = Source.MyButton(frame, text=text, width=30, command=command)
        func_button.place(x=140, y=2)
        close_button = Source.MyButton(frame, text='Закрыть', width=10,  command=self.destroy)
        close_button.place(x=418, y=2)
        frame.pack()

    def __show_label_widget(self, text, x_pos, y_pos):
        """Конструктор текстового лейбла"""
        text_label = Source.ttk.Label(self.product_menus_frame, text=text)
        text_label.place(x=x_pos, y=y_pos)

    def __show_entry_frame(self, txt_var_name, text, x, y, width=39, state='normal'):
        """Конструктор фрейма для отрисовки Entry виджета"""
        self.__show_label_widget(text, x, y)
        self.product_menus_frame.__dict__[txt_var_name] = Source.tk.StringVar(self.product_menus_frame)
        entry = Source.ttk.Entry(self.product_menus_frame, width=width, state=state,
                                 textvariable=self.product_menus_frame.__dict__[txt_var_name])
        entry.place(x=x, y=y + 20)

    def __show_combobox_frame(self, cb_var, text, x, y, cb_val):
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        self.__show_label_widget(text, x, y)
        self.product_menus_frame.__dict__[cb_var] = Source.ttk.Combobox(self.product_menus_frame, width=36,
                                                                        state="readonly", values=cb_val)
        self.product_menus_frame.__dict__[cb_var].place(x=x, y=y + 20)

    def __show_check_frame(self, var, text, x, y):
        """Конструктор для отрисовки чек фреймов"""
        self.product_menus_frame.__dict__[var] = Source.tk.IntVar(self.product_menus_frame)
        check_btn = Source.tk.Checkbutton(self.product_menus_frame, text=text,
                                          variable=self.product_menus_frame.__dict__[var])
        check_btn.place(x=x, y=y)

    def __show_radio_frame(self, radio_var, text, x, y, radio_val):
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        self.__show_label_widget(text, x, y)
        self.product_menus_frame.__dict__[radio_var] = Source.tk.StringVar(self.product_menus_frame, value=radio_val[0])
        indent = {'segment': ((0, 20), (80, 20)),
                  'book_option': ((0, 20), (50, 20), (100, 20)),
                  'lamination': ((0, 20), (50, 20), (100, 20)),
                  'cover_type': ((0, 20), (0, 40), (0, 60), (80, 20), (80, 40))}[radio_var]
        for i, name in enumerate(radio_val):
            i_x, i_y = indent[i]
            x_pos, y_pos = x + i_x, y + i_y
            radio = Source.ttk.Radiobutton(self.product_menus_frame, text=name, value=name,
                                           variable=self.product_menus_frame.__dict__[radio_var])
            radio.place(x=x_pos, y=y_pos)

    def init_menu_lines(self):
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        for key, value in self.product_obj.__dict__.items():
            tip, *attr = self.__FRAMES.get(key)
            if key == 'full_name' and type(self) == ChangeLibWindow:
                attr.append(Source.tk.DISABLED)
            if tip == 'entry':
                self.__show_entry_frame(key, *attr)
            if tip == 'combo':
                self.__show_combobox_frame(key, *attr, value)
            if tip == 'check':
                self.__show_check_frame(key, *attr)
            if tip == 'radio':
                self.__show_radio_frame(key, *attr, value)
        separator = Source.tk.Canvas(self.product_menus_frame, width=496, height=1, bg='black')
        separator.place(x=0, y=248)

    def insert_values_from_lib(self, prod_descr):
        """Метод для вставки полученных значений в бд"""
        for key, value in self.lib.get_product_values(*prod_descr).items():
            self.product_menus_frame.__dict__[key].set(value)

    def get_values_from_widgets(self) -> dict | None:
        """Метод для получения информации из введеных менюшек"""
        if not self.product_obj:
            return
        dct = {}
        required = ('full_name', 'segment', 'short_name', 'product_format', 'book_option', 'lamination',
                    'cover_print_mat', 'cover_carton', 'page_print_mat', 'cover_type', 'cover_canal', 'page_canal')
        numbered = ('gl_pos', 'gl_len', 'dc_overlap', 'dc_top_indent', 'dc_left_indent')
        for key in self.product_obj.__dict__.keys():
            value = self.product_menus_frame.__dict__[key].get()
            if key in required and value or key == 'dc_break':
                dct[key] = value
            elif key in numbered:
                dct[key] = int(value) if value.isdigit() else 0
            else:
                return
        return dct


class AddToLibWindow(AssistWindow):
    """Окно для добавления продукта в библиотеку"""
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.category_combobox = None
        self.main()

    def main(self):
        self.title('Добавление продукта в библиотеку')
        self.show_category_frame()
        self.product_menus_frame.pack()
        self.show_buttons('Добавить', self.add_btn)
        self.to_parent_center()
        self.focus()

    def show_category_frame(self):
        """Функция для обображения фрейма категорий. Инициализирует комбобокс с нужным Событием."""
        label = Source.tk.Label(self, text='Выберите категорию')
        label.pack()
        self.category_combobox = Source.ttk.Combobox(self, state="readonly", width=40,
                                                     values=tuple(x.name for x in self.lib.get_product_objects_list()))
        self.category_combobox.bind('<<ComboboxSelected>>', self.set_product_obj_from_combobox)
        self.category_combobox.pack()
        separator = Source.tk.Canvas(self, width=496, height=1, bg='black')
        separator.pack()

    def set_product_obj_from_combobox(self, event=None):
        """Установка объекта продукта исходя из выбранного значения в комбобоксе"""
        self.product_obj = self.lib.get_product_object(self.category_combobox.get())
        self.product_menus_frame_clearing()
        self.init_menu_lines()

    def add_btn(self):
        """Операции кнопки добавления продукта в бд"""
        dct = self.get_values_from_widgets()
        # Проверяем на то, что получены все значения и этот продукт уникальный
        if dct:
            if self.lib.check_unique(self.product_obj.category, dct['full_name']):
                self.lib.add(self.product_obj.category, dct)
                Source.tkmb.showinfo('Добавление продукта', f'{dct["full_name"]}\nУспешно добавлено в библиотеку')
                if type(self) == AddToLibWindow:
                    self.set_product_obj_from_combobox()
            else:
                Source.tkmb.showerror('Проверка на дубликат', f'{dct["full_name"]}\nприсутствует в библиотеке')
        self.focus()


class CopyFromLibWindow(AddToLibWindow):
    """Окно для создания нового продукта на основе имеющегося"""
    def __init__(self, parent_root, product_descr):
        self.product_descr = product_descr
        super().__init__(parent_root)

    def main(self):
        self.title('Добавление нового продукта')
        self.product_menus_frame.pack()
        self.show_buttons('Добавить', self.add_btn)
        self.product_obj = self.lib.get_product_object(self.product_descr[0])
        self.init_menu_lines()
        self.insert_values_from_lib(self.product_descr)
        self.to_parent_center()
        self.focus()


class ChangeLibWindow(AssistWindow):
    """Окно для внесения изменения в продукт"""
    def __init__(self, parent_root, product_descr):
        super().__init__(parent_root)
        self.title('Изменение значений продукта')
        self.product_menus_frame.pack()
        self.show_buttons('Изменить', self.change_btn)
        self.product_obj = self.lib.get_product_object(product_descr[0])
        self.init_menu_lines()
        self.insert_values_from_lib(product_descr)

    def change_btn(self):
        """Операции кнопки изменения значений продукта"""
        dct = self.get_values_from_widgets()
        if dct:
            category, name = self.product_obj.category, dct.pop('full_name')
            self.lib.change(category, name, dct)
            Source.tkmb.showinfo('Изменение значений продукта', f'{name}\nДанные успешно обновленны')
        self.focus()
