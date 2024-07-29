import re
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd
from tkinter import colorchooser as tkcc

import modules.Configs as Conf
import modules.Roddom as Roddom
import modules.FileProcessor as FileProc
import modules.Library as Lib
import modules.LogCreator as Log
import modules.Information as Inf


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SETTINGS = Conf.read_pcl('settings')        # Сохраняем как атрибут ссылку на настройки и библиотеку
        self.LIBRARY = Conf.read_pcl('library')
        self.init_cells()
        self.show_menus()
        self.set_main_graph_settings()

    def init_cells(self):
        def init_roddom_window(): RoddomWindow(self)

        def init_log(): Log.main()

        def init_sticgen(): StickerGenWindow(self)

        def init_smart_proc_window(): SmartProcWindow(self)

        def init_backup_window(): BackUpWindow(self)

        def init_mail_samples_win(): MailSamplesWindow(self)

        info_cell_label = CellLabel(master=self, label_text='Работа с заказами', label_color='#ed95b7')
        info_cell_label.pack()
        info_cell = CellTwoButton(master=self, bt_l_name='Обновить БД', bt_r_name='СтикГен',
                                  bt_l_func=init_log, bt_r_func=init_sticgen)
        info_cell.pack()
        smart_proc_label = CellLabel(master=self, label_color='dark salmon', label_text='Умная обработка')
        smart_proc_label.pack()
        smart_button = CellOneButton(master=self, func_name='Подготовка к печати', pd_x=10, func=init_smart_proc_window)
        smart_button.pack()
        bup_label = CellLabel(master=self, label_color='#adc6ed', label_text='Бакап файлов заказа')
        bup_label.pack()
        bup_button = CellOneButton(master=self, func_name='Подготовка к печати', pd_x=10, func=init_backup_window)
        bup_button.pack()
        fotoprint_label = CellLabel(master=self, label_color='pale green', label_text='Фотопечать')
        fotoprint_label.pack()
        roddom_cell = CellOneButton(master=self, func_name='Роддом', func=init_roddom_window, pd_x=50)
        roddom_cell.pack()
        social_label = CellLabel(master=self, label_color='#7683de', label_text='Общение', )
        social_label.pack()
        mail_sample_btn = CellOneButton(master=self, func_name='Текстовые шаблоны', pd_x=10, func=init_mail_samples_win)
        mail_sample_btn.pack()

    def set_main_graph_settings(self):
        self.title('Органайзер 2_0 BETA')
        width, height = 270, 266
        self.geometry(f'{width}x{height}+'
                      f'{(self.winfo_screenwidth() - width) // 2}+'
                      f'{(self.winfo_screenheight() - height) // 2}')
        self.resizable(False, False)

    def show_menus(self):
        def init_settings_window(): SettingsWindow(self)

        def init_add_to_lib_window(): AddToLibWindow(self)

        def init_change_lib_window(): ChangeLibWindow(self)

        def init_delete_from_lib_window(): DeleteFromLibWindow(self)

        def init_information_window(): InformationWindow(self)

        settings_menu = tk.Menu(tearoff=0)
        settings_menu.add_command(label="Общие настройки", command=init_settings_window)

        library_menu = tk.Menu(tearoff=0)
        library_menu.add_command(label='Добавить продукт', command=init_add_to_lib_window)
        library_menu.add_command(label='Изменить продукт', command=init_change_lib_window)
        library_menu.add_command(label='Удалить продукт', command=init_delete_from_lib_window)

        information_menu = tk.Menu(tearoff=0)
        information_menu.add_command(label='Информация по продуктам', command=init_information_window)

        main_menu = tk.Menu()
        main_menu.add_cascade(label="Настройки", menu=settings_menu)
        main_menu.add_cascade(label='Библиотека', menu=library_menu)
        main_menu.add_cascade(label='Информация', menu=information_menu)
        self.config(menu=main_menu)


class CellLabel(tk.Frame):
    """Конструктор для ячеек с названиями"""

    def __init__(self, label_color='red', label_text='Название лейбла', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = tk.Label(self, text=label_text, bg=label_color, width=270)
        self.label.pack()


class CellOneButton(tk.Frame):
    """Конструктор для одиночных кнопок"""

    def __init__(self, func_name='Название кнопки', func=None, pd_x=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=270)
        self.button = tk.Button(self, text=func_name, relief=tk.FLAT, fg="#eee", bg="#454545", command=func, padx=pd_x)
        self.button.pack(pady=3)


class CellTwoButton(tk.Frame):
    """Конструктор для парных кнопок"""

    def __init__(self, bt_l_name='Название кнопки', bt_l_func=None, bt_r_name='Название кнопки', bt_r_func=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=270)
        self.l_button = tk.Button(self, text=bt_l_name, command=bt_l_func, relief=tk.FLAT, fg="#eee", bg="#454545")
        self.l_button.pack(side='left', ipadx=20, padx=10, pady=3)
        self.r_button = tk.Button(self, text=bt_r_name, command=bt_r_func, relief=tk.FLAT, fg="#eee", bg="#454545")
        self.r_button.pack(side='right', ipadx=20, padx=10, pady=3)


class ChildWindow(tk.Toplevel):
    """Конструктор для дочерних окон"""

    def __init__(self, parent_root):
        self.parent_root = parent_root
        super().__init__(master=parent_root)
        self.style = {'relief': tk.FLAT, 'fg': "#eee", 'bg': "#454545"}

    def to_parent_center(self):
        """Центрирование относительно родительского окна"""
        self.update_idletasks()
        parent_width = self.parent_root.winfo_width()  # Получаем размер родительского окна
        parent_height = self.parent_root.winfo_height()
        parent_place_x = self.parent_root.winfo_x()  # Получаем положение родительского окна
        parent_place_y = self.parent_root.winfo_y()
        child_width = self.winfo_width()  # Размер дочернего окна
        child_height = self.winfo_height()
        place_x = ((parent_width - child_width) // 2) + parent_place_x
        place_y = ((parent_height - child_height) // 2) + parent_place_y
        self.geometry(f"+{place_x}+{place_y}")

    def focus(self):
        """Перехват фокуса и блокирование родительского окна"""
        self.grab_set()
        self.focus_set()
        self.wait_window()


class RoddomWindow(ChildWindow):
    """Окно Роддома"""

    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.order_exist = None         # Переменные, которые используют виджеты
        self.directory_info = tk.StringVar(self, self.parent_root.SETTINGS['roddom_main_dir'])
        self.order_calc_info = None
        self.text_res_enable = tk.BooleanVar(self, value=True)
        self.mrk_form_enable = tk.BooleanVar(self, value=False)
        self.__main()

    def __main(self):
        self.title('Роддом')
        self.geometry('260x237')
        self.resizable(False, False)
        self.to_parent_center()
        self.show_directory_widget()
        self.info_frame = tk.Frame(self, width=260, height=80)
        self.info_frame.pack()
        self.show_cb_frame()
        self.show_buttons_widget()
        self.focus()

    def show_directory_widget(self):
        """Функция отрисовки фрейма с информацией, где храняться заказы роддома"""
        frame = tk.Frame(self, width=260, height=50)
        dir_status_label = tk.Label(frame, text='Папка, куда сохраняются заказы Роддом\'а')
        dir_status_label.place(x=0, y=0)
        dir_update_button = tk.Button(frame, textvariable=self.directory_info, command=self.update_directory,
                                      width=35, **self.style)
        dir_update_button.place(x=3, y=20)
        separator = tk.Canvas(frame, width=260, height=1, bg='black')
        separator.place()
        frame.pack()

    def update_directory(self):
        """Функция смены папки размещения заказов роддома"""
        new_path = tkfd.askdirectory()
        if new_path:
            self.directory_info.set(new_path)
            self.parent_root.SETTINGS['roddom_main_dir'] = new_path
            Conf.write_pcl('settings', self.parent_root.SETTINGS)

    def show_cb_frame(self):
        """Функция отрисовки Checkbutton - настроек обработки заказов роддома"""
        frame = tk.Frame(self, width=260, height=50)
        separator = tk.Canvas(frame, width=260, height=1, bg='black')
        separator.place(x=0, y=0)
        text_res_cb = ttk.Checkbutton(frame, text='Сохранять результаты в sum.txt', variable=self.text_res_enable)
        text_res_cb.place(x=3, y=3)
        mrk_form_cb = ttk.Checkbutton(frame, text='Формировать .mrk файл', variable=self.mrk_form_enable)
        mrk_form_cb.place(x=3, y=23)
        frame.pack()

    def show_buttons_widget(self):
        """Функция отрисовки кнопок, для взаимодействия с заказом"""
        frame = tk.Frame(self, width=260, height=60)
        button1 = tk.Button(frame, text='Посчитать заказ', command=self.init_calc, **self.style)
        button1.place(x=3, y=0)
        button2 = tk.Button(frame, text='Скопировать инф', command=self.info_to_clipboard, **self.style)
        button2.place(x=3, y=28)
        button3 = tk.Button(frame, text='Отправить в печать', command=self.to_print, **self.style)
        button3.place(y=28, x=138)
        frame.pack()

    def init_calc(self):
        """Функция вызова метода подсчета из заказа - объекта Роддома"""
        order = tkfd.askdirectory(initialdir=self.directory_info.get())
        if not order:
            return
        self.order_exist = Roddom.RoddomOrder(order, self.text_res_enable.get(), self.mrk_form_enable.get())
        self.order_calc_info = str(self.order_exist)
        self.show_order_info(self.order_calc_info)
        self.info_to_clipboard()

    def info_to_clipboard(self):
        """Функция, которая заносит информацию о пути и дате заказа в будфер обмена"""
        tk.Tk.clipboard_clear(self)
        tk.Tk.clipboard_append(self, self.order_calc_info)

    def info_frame_clear(self):
        """Функция очистки info_frame"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()

    def show_order_info(self, text):
        """Функция отрисовки подсчитанной информации"""
        self.info_frame_clear()
        label = tk.Label(self.info_frame, text=text, font=12)
        label.place(x=0, y=0)

    def button_disabler(self):
        """Функция, которая выключает взаимодействие с кнопками"""
        for i in self.winfo_children():
            if type(i) == tk.Frame:
                for j in i.winfo_children():
                    if type(j) == tk.Button and j.__dict__['_name'] != '!button2':
                        j.config(state="disabled")

    def button_enabler(self):
        """Функция, которая включает взаимодействие с кнопками"""
        for i in self.winfo_children():
            if type(i) == tk.Frame:
                for j in i.winfo_children():
                    if type(j) == tk.Button and j.__dict__['_name'] != '!button2':
                        j.config(state="normal")

    def to_print(self):
        """Функция отправки в печать. Отображает на экране информацию о коопировани и вызывает методы копирования"""
        path = tkfd.askdirectory(initialdir=self.parent_root.SETTINGS['fotoprint_temp_dir'])
        if not path or not self.order_exist:
            return
        self.order_calc_info = f'{path}\n\nРоддом\n\n{self.order_exist.order_name}'
        self.info_to_clipboard()
        self.info_frame_clear()
        self.button_disabler()
        operation_label = tk.Label(self.info_frame, text='Создаю Каталоги')
        operation_label.place(x=0, y=0)
        file_label = tk.Label(self.info_frame, text='Вторая строчка')
        file_label.place(x=0, y=15)
        progressbar = ttk.Progressbar(self.info_frame, orient=tk.HORIZONTAL, mode="determinate", length=254)
        progressbar.place(x=3, y=40)
        for i in self.order_exist.get_directory_list():
            FileProc.make_dirs(f'{path}/{i}')
        file_lst = self.order_exist.get_file_list()
        file_len = len(file_lst)
        progressbar['maximum'] = file_len
        progressbar['value'] = 0
        operation_label.config(text='Копирую файлы')
        for name in file_lst:
            FileProc.shutil_copy2(f'{self.directory_info.get()}/{name}', f'{path}/{name}')
            progressbar['value'] += 1
            file_label.config(text=f'{progressbar["value"]}/{file_len} -- {name.split("/")[-1]}')
            self.update()
        operation_label.config(text='Завершено')
        file_label.config(text='')
        self.button_enabler()
        self.order_exist = None


class SettingsWindow(ChildWindow):
    """Окно основных настроек приложения"""
    def __init__(self, main_window):
        super().__init__(main_window)
        self.__main()

    def __main(self):
        self.title('Настройки')
        self.show_autolog_widget()
        self.show_log_check_depth_widget()
        self.show_cover_proc_settings('Цвет обводки', 'stroke_color', 'Толщина обводки', 'stroke_size')
        self.show_cover_proc_settings('Цвет направляющих', 'guideline_color', 'Толщина направляющих', 'guideline_size')
        self.show_directory_widget('Диск оператора фотопечати', 'fotoprint_temp_dir')
        self.show_directory_widget('Папка для сохранения заказов', 'order_main_dir')
        self.to_parent_center()
        self.resizable(False, False)
        self.focus()

    def show_autolog_widget(self):
        """Функция отрисовки виджета управления Автологом"""
        def update_label_info():
            autolog = self.parent_root.SETTINGS['autolog']
            autolog_label.config(text='Автолог: Активен' if autolog else 'Автолог: Отключен')
            autolog_init_bt.config(text='Отключить' if autolog else 'Включить')

        def init_autolog():
            value = not self.parent_root.SETTINGS['autolog']
            self.parent_root.SETTINGS['autolog'] = value
            update_label_info()
            Conf.write_pcl('settings', self.parent_root.SETTINGS)
            tkmb.showinfo('Автолог', 'Функция автолога отключена. Пожалуйста, обновляйте лог вручную.')

        frame = tk.Frame(self, width=260, height=30)
        autolog_label = tk.Label(frame)
        autolog_label.place(x=0, y=4)
        autolog_init_bt = tk.Button(frame, **self.style, command=init_autolog)
        autolog_init_bt.place(x=130, y=2)
        update_label_info()
        separator = tk.Canvas(frame, width=260, height=1, bg='black')
        separator.place(x=0, y=27)
        frame.pack()

    def show_log_check_depth_widget(self):
        """Функция управления глубиной проверки заказов"""
        def update_text_value():
            label.config(text=f'Глубина проверки лога - {self.parent_root.SETTINGS["log_check_depth"]} заказов')

        def update_depth_value():
            value = entry_var.get()
            if value.isdigit():
                self.parent_root.SETTINGS['log_check_depth'] = int(value)
                Conf.write_pcl('settings', self.parent_root.SETTINGS)
            update_text_value()
            entry.delete(0, tk.END)

        frame = tk.Frame(self, width=260, height=51)
        label = tk.Label(frame)
        label.place(x=1, y=1)
        update_text_value()
        entry_var = tk.StringVar(frame)
        entry = tk.Entry(frame, width=10, textvariable=entry_var)
        entry.place(x=40, y=26)
        update_button = tk.Button(frame, text='Задать', **self.style, command=update_depth_value)
        update_button.place(x=120, y=22)
        separator = tk.Canvas(frame, width=260, height=1, bg='black')
        separator.place(x=0, y=47)
        frame.pack()

    def show_cover_proc_settings(self, color_text, color_stg_key, size_text, size_stg_key):
        """Функция-конструктор для управления цветом и толщиной для направляющих и обводки"""
        def update_color():
            color = tkcc.askcolor()
            if color:
                self.parent_root.SETTINGS[color_stg_key] = color[1]
                Conf.write_pcl('settings', self.parent_root.SETTINGS)
            color_btn.config(bg=self.parent_root.SETTINGS[color_stg_key])

        def update_size_label():
            size_label.config(text=f'{size_text}: {self.parent_root.SETTINGS[size_stg_key]} пикселей')

        def update_size(val):
            self.parent_root.SETTINGS[size_stg_key] = int(val)
            Conf.write_pcl('settings', self.parent_root.SETTINGS)
            update_size_label()

        frame = tk.Frame(self, width=260, height=73)
        label = tk.Label(frame, text=color_text)
        label.place(x=1, y=3)
        color_btn = tk.Button(frame, relief=tk.FLAT, width=12, bg=self.parent_root.SETTINGS[color_stg_key],
                              command=update_color)
        color_btn.place(x=125, y=0)
        size_label = tk.Label(frame)
        size_label.place(x=1, y=26)
        scale = tk.Scale(frame, orient=tk.HORIZONTAL, from_=1, to=10, length=255, showvalue=False, command=update_size)
        scale.place(x=0, y=48)
        scale.set(self.parent_root.SETTINGS[size_stg_key])
        update_size_label()
        separator = tk.Canvas(frame, width=260, height=1, bg='black')
        separator.place(x=0, y=68)
        frame.pack()

    def show_directory_widget(self, text, settings_key):
        """Функция-конструктор для управления основными дирректориями"""
        def update_directory():
            path = tkfd.askdirectory()
            if path:
                text_var.set(path)
                self.parent_root.SETTINGS[settings_key] = path
                Conf.write_pcl('settings', self.parent_root.SETTINGS)

        frame = tk.Frame(self, width=260, height=50)
        text_var = tk.StringVar(frame, value=self.parent_root.SETTINGS[settings_key])
        dir_status_label = tk.Label(frame, text=text)
        dir_status_label.place(x=0, y=0)
        dir_update_button = tk.Button(frame, textvariable=text_var, command=update_directory, width=35, **self.style)
        dir_update_button.place(x=3, y=20)
        separator = tk.Canvas(frame, width=260, height=1, bg='black')
        separator.place(x=0, y=45)
        frame.pack()


class LibraryWindow(ChildWindow):
    """Конструктор для окон библиотеки"""
    __FRAMES = {'segment': ('combo', 'Выберите сегмент продукции', 4, 41),
                'short_name': ('combo', 'Выберите короткое имя', 4, 82),
                'book_format': ('combo', 'Выберите формат книги', 4, 123),
                'book_option': ('radio', 'Выберите опции сборки книги', 4, 164),
                'lamination': ('radio', 'Выберите ламинацию для продукта', 4, 205),
                'cover_print_mat': ('combo', 'Выберите печатный материал обложки', 256, 41),
                'cover_carton': ('combo', 'Выберите картонку для обложки', 256, 82),
                'page_print_mat': ('combo', 'Выберите печатный материал разворотов', 256, 123),
                'dc_break': ('check', 'Раскодировка с дублированием', 270, 221),
                'book_type': ('radio', 'Выберите тип обложки', 256, 164),
                'gl_value': ('entry', "Введите значение в мм для направляющих", 4, 251),
                'gl_length': ('entry', 'Введите длинну направляющих в мм', 4, 292),
                'cover_canal': ('combo', "Выберите 'канал' обложки", 256, 251),
                'page_canal': ('combo', "Выберите 'канал' разворотов", 256, 292),
                'dc_overlap': ('entry', 'НАХЛЕСТ для переплета в мм', 256, 251),
                'dc_top_indent': ('entry', 'Введите значение отступа СВЕРХУ в мм', 256, 292),
                'dc_left_indent': ('entry', 'Введите значение отступа СЛЕВА в мм', 256, 333)
                }

    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.product_description = None  # Для хранения словаря с описанием категорий продукта и типов значений
        # Переменные, которые заполняются в зависимости от выбранного окна и выбранного действия
        self.category_combobox = None  # Для отрисовки комбобокса категорий и сохранения его значений
        self.names_combobox = None  # Для отрисовки комбобокса с сохраненными именами продуктов
        self.product_menus_frame = None  # Фрейм, на котором рисуются менюшки с выбором
        self.product_name_entry = None
        self.resizable(False, False)

    def show_category_frame(self, cb_bind_func):
        """Функция для обображения фрейма категорий. Инициализирует комбобокс с нужным Событием."""
        frame = tk.Frame(self, width=500, height=51)
        label = tk.Label(frame, text='Выберите категорию')
        label.place(x=200, y=1)
        self.category_combobox = ttk.Combobox(frame, state="readonly", width=40, values=Lib.Product.RUS_NAMES)
        self.category_combobox.bind('<<ComboboxSelected>>', cb_bind_func)
        self.category_combobox.place(x=130, y=25)
        separator = tk.Canvas(frame, width=496, height=1, bg='black')
        separator.place(x=0, y=46)
        frame.pack()

    def show_saved_names_frame(self, cb_bind_func):
        """Функция для отрисовки фрейма с отображением сохраненных имен"""
        frame = tk.Frame(self, width=500, height=50)
        label = tk.Label(frame, text='Выберите продукт')
        label.place(x=200, y=1)
        self.names_combobox = ttk.Combobox(frame, state="readonly", width=79)
        self.names_combobox.bind('<<ComboboxSelected>>', cb_bind_func)
        self.names_combobox.place(x=2, y=25)
        separator = tk.Canvas(frame, width=496, height=1, bg='black')
        separator.place(x=0, y=46)
        frame.pack()

    def show_product_menus(self):
        """Функция для отрисовки фрейма менюшек выбора значений"""
        self.product_menus_frame = tk.Frame(self, width=500, height=380)
        self.product_menus_frame.pack()

    def show_buttons(self, text, command):
        """Функция для отрисовки кнопок"""
        frame = tk.Frame(self, width=500, height=30)
        frame.pack()
        button = tk.Button(frame, **self.style, text=text, width=30, command=command)
        button.place(x=140, y=2)

    def product_menus_frame_clearing(self):
        """Очистка меню-виджета от ненужных фреймов"""
        for widget in self.product_menus_frame.winfo_children():
            widget.destroy()

    def __show_entry_frame(self, text, txt_var_name, x, y, width=39):
        """Конструктор фрейма для отрисовки Entry виджета"""
        text_label = ttk.Label(self.product_menus_frame, text=text)
        text_label.place(x=x, y=y)
        self.__dict__[txt_var_name] = tk.StringVar(self.product_menus_frame)
        entry = ttk.Entry(self.product_menus_frame, width=width, textvariable=self.__dict__[txt_var_name])
        entry.place(x=x, y=y + 20)

    def __show_combobox_frame(self, text, cb_var, cb_val, x, y):
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        text_label = tk.Label(self.product_menus_frame, text=text)
        text_label.place(x=x, y=y)
        self.__dict__[cb_var] = ttk.Combobox(self.product_menus_frame, width=36, state="readonly", values=cb_val)
        self.__dict__[cb_var].place(x=x, y=y + 20)

    def __show_check_frame(self, text, var, x, y):
        """Конструктор для отрисовки чек фреймов"""
        self.__dict__[var] = tk.BooleanVar(self.product_menus_frame)
        check_btn = tk.Checkbutton(self.product_menus_frame, text=text, variable=self.__dict__[var])
        check_btn.place(x=x, y=y)

    def __show_radio_frame(self, text, radio_var, radio_val, x, y):
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        text_label = tk.Label(self.product_menus_frame, text=text)
        text_label.place(x=x, y=y)
        self.__dict__[radio_var] = tk.StringVar(self.product_menus_frame, value=radio_val[0])
        indents = ((0, 20), (50, 20), (100, 20))
        if radio_var == '_book_type':
            indents = ((0, 20), (0, 40), (80, 20), (80, 40), (0, 60))
        for i, name in enumerate(radio_val):
            i_x, i_y = indents[i]
            x_pos, y_pos = x + i_x, y + i_y
            radio = ttk.Radiobutton(self.product_menus_frame, text=name, value=name, variable=self.__dict__[radio_var])
            radio.place(x=x_pos, y=y_pos)

    def init_menu_lines(self):
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        setattr(self, '_product_name', None)
        self.__show_entry_frame('Введите полное имя продукта', '_product_name', 4, 0, 81)
        for key in self.product_description.keys():
            if key == 'category':
                continue
            var = f'_{key}'
            tip, text, x, y = self.__FRAMES.get(key)
            setattr(self, var, None)
            if tip == 'entry':
                self.__show_entry_frame(text, var, x, y)
            if tip == 'combo':
                self.__show_combobox_frame(text, var, getattr(Lib.Product, key.upper()), x, y)
            if tip == 'check':
                self.__show_check_frame(text, var, x, y)
            if tip == 'radio':
                self.__show_radio_frame(text, var, getattr(Lib.Product, key)(self.category_combobox.get()), x, y)
        separator = tk.Canvas(self.product_menus_frame, width=496, height=1, bg='black')
        separator.place(x=0, y=248)

    def get_values_from_menus(self):
        """Получение введенных значений"""
        category = self.category_combobox.get()
        if not category:
            return
        full_name = getattr(self, '_product_name').get()
        values = {}
        for key in self.product_description:
            if key == 'category':
                values[key] = self.product_description[key]
                continue
            value = self.__dict__[f'_{key}'].get()
            if key in ('gl_value', 'gl_length', 'dc_overlap', 'dc_top_indent', 'dc_left_indent'):
                value = int(value) if value.isdigit() else 0
            if value or key in ('dc_break', 'gl_value', 'gl_length', 'dc_overlap', 'dc_top_indent', 'dc_left_indent'):
                values[key] = value
        if len(values) != len(self.product_description) or not full_name:
            return
        return {full_name: values}

    def clear_menus_entered_values(self):
        """Установка значений в комбобоксах и энтри на пустые"""
        self.__dict__['_product_name'].set('')
        for key in self.product_description:
            frame = self.__FRAMES.get(key)
            if frame and frame[0] in ('combo', 'entry'):
                self.__dict__[f'_{key}'].set('')

    def set_values_to_enter_menus(self, name):
        """Установка значений в комбобоксах и энтри на сохраненные"""
        self.__dict__['_product_name'].set(name)
        product_dict = self.parent_root.LIBRARY[name]
        for key in self.product_description:
            if key == 'category':
                continue
            self.__dict__[f'_{key}'].set(product_dict[key])

    def save_library(self):
        """Пишем в Либу"""
        Conf.write_pcl('library', self.parent_root.LIBRARY)


class AddToLibWindow(LibraryWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Добавление продукта')
        self.show_category_frame(self.category_event)
        self.show_product_menus()
        self.show_buttons('Сохранить продукт в библиотеке', self.add_button)
        self.to_parent_center()
        self.focus()

    def category_event(self, event=None):
        self.product_menus_frame_clearing()
        self.product_description = Lib.Product.get_product_descr(self.category_combobox.get())
        self.init_menu_lines()

    def add_button(self):
        dct = self.get_values_from_menus()
        if dct:
            self.parent_root.LIBRARY.update(dct)
            self.save_library()
            self.clear_menus_entered_values()
            tkmb.showinfo(title='Добавление продукта', message='Продукт успешно добавлен в библиотеку')


class ChangeLibWindow(LibraryWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Измeнение продукта')
        self.show_category_frame(self.category_event)
        self.show_saved_names_frame(self.names_event)
        self.show_product_menus()
        self.show_buttons('Обновить значения', self.change_button)
        self.to_parent_center()
        self.focus()

    def category_event(self, event):
        self.names_combobox.set('')
        category = Lib.Product.CATEGORY[Lib.Product.RUS_NAMES.index(self.category_combobox.get())]
        names = sorted(k for k, v in self.parent_root.LIBRARY.items() if v['category'] == category)
        self.names_combobox.config(values=names)
        self.product_menus_frame_clearing()

    def names_event(self, event=None):
        name = self.names_combobox.get()
        if name:
            self.product_menus_frame_clearing()
            self.product_description = Lib.Product.get_product_descr(self.category_combobox.get())
            self.init_menu_lines()
            self.set_values_to_enter_menus(name)

    def change_button(self):
        dct = self.get_values_from_menus()
        if dct:
            self.parent_root.LIBRARY.pop(self.names_combobox.get())
            self.parent_root.LIBRARY.update(dct)
            self.clear_menus_entered_values()
            self.save_library()
            self.category_event(None)
            tkmb.showinfo(title='Изменение продукта', message='Значения продукта успешно обновлены')


class DeleteFromLibWindow(LibraryWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Удаление продукта')
        self.show_category_frame(self.category_event)
        self.show_saved_names_frame(None)
        self.show_buttons('Удалить продукт из библиотеки', self.del_button)
        self.to_parent_center()
        self.focus()

    def category_event(self, event=None):
        self.names_combobox.set('')
        category = Lib.Product.CATEGORY[Lib.Product.RUS_NAMES.index(self.category_combobox.get())]
        names = sorted(k for k, v in self.parent_root.LIBRARY.items() if v['category'] == category)
        self.names_combobox.config(values=names)

    def del_button(self):
        product_to_del = self.names_combobox.get()
        if product_to_del:
            self.parent_root.LIBRARY.pop(product_to_del)
            self.save_library()
            self.names_combobox.set('')
            self.category_event()
            tkmb.showinfo(title='Удаление продукта', message='Продукт удален из библиотеки')


class StickerGenWindow(ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.transient(parent_root)
        self.order_name = tk.StringVar()
        self.order_info = tk.StringVar()
        self.__main()

    def __main(self):
        self.title('Генерация наклеек')
        self.show_order_entry_frame()
        self.show_order_info_frame()
        self.show_buttons_frame()
        self.resizable(False, False)
        self.to_parent_center()
        self.grab_set()
        self.wait_window()

    def show_order_entry_frame(self):
        frame = tk.Frame(master=self, height=52, width=300)
        label = tk.Label(frame, text='Введите номер заказа')
        label.place(x=86, y=1)
        entry = tk.Entry(frame, textvariable=self.order_name)
        entry.place(x=55, y=27)
        entry.bind('<Return>', self.get_order_info)
        entry.focus_set()
        button = tk.Button(frame, text='Получить', **self.style, command=self.get_order_info)
        button.place(x=185, y=24)
        frame.pack()

    def get_order_info(self, event=None):
        order_name = self.order_name.get()
        for log_dict in Conf.read_pcl_log_for_processing():
            if order_name in log_dict:
                self.order_info.set(Inf.StickerInfo(order_name, log_dict[order_name], self.parent_root.LIBRARY).main())
                break
        self.order_name.set('')
        self.to_clipboard()

    def show_order_info_frame(self):
        frame = tk.Frame(self, width=300, height=200)
        frame.pack()
        label = tk.Label(frame, justify=tk.LEFT, textvariable=self.order_info)
        label.place(x=1, y=1)

    def show_buttons_frame(self):
        frame = tk.Frame(self, width=300, height=28)
        button1 = tk.Button(frame, text='Скопировать в буфер', **self.style, command=self.to_clipboard)
        button1.place(x=1, y=1)
        button2 = tk.Button(frame, text='Закрыть', **self.style, command=self.destroy)
        button2.place(x=242, y=1)
        frame.pack()

    def to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.order_info.get())


class ProcessingWindow(ChildWindow):
    """Конструктор для окон обработчика заказов"""

    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.order_name_label = None  # Общие переменные для вывода информации
        self.order_name_entry_var = tk.StringVar(self)
        self.order_exist = None
        self.init_local_variables()  # Инициализируем локальные переменные
        self.processing_info = None
        self.processing_pb = None
        self.__main()
        self.event_flag = True

    def init_local_variables(self):
        """Абстракнтная функция для запуска локальных переменных (в дочерних классах)"""
        pass

    def reset_settings_to_default(self):
        """Абстрактная функция для сброса значений локальных переменных"""
        pass

    def show_main_frame(self):
        """Абстрактная функция отрисовки основного виджета дочернего обработчика"""
        pass

    def get_order_settings(self):
        """Абстрактная функция для получения словаря значений переменых в дочерних классах"""
        pass

    def __main(self):
        """Инициализация виджетов"""
        self.config(border=1, relief='solid')
        self.order_name_entry_widget()
        self.order_name_label = ttk.Label(master=self, text='Для запуска обработчика введите номер заказа')
        self.order_name_label.pack()
        self.show_main_frame()
        self.buttons_frame()
        self.overrideredirect(True)
        self.to_parent_center()
        self.bind('<Control-Return>', self.init_proc)

    def order_name_entry_widget(self):
        """Функция отрисовки виджета ввода номера заказа"""
        frame = tk.Frame(master=self, width=300, height=30)
        label = ttk.Label(master=frame, text='Введите номер заказа:')
        label.place(x=20, y=4)
        entry = ttk.Entry(master=frame, width=10, textvariable=self.order_name_entry_var)
        entry.bind("<Return>", self.get_order_dict)
        entry.bind('<Control-Return>', self.init_proc)
        entry.focus_set()
        entry.place(x=150, y=4)
        button = tk.Button(master=frame, **self.style, text='Ввод', padx=10, command=self.get_order_dict)
        button.place(x=220, y=1)
        canvas = tk.Canvas(master=frame, width=296, height=1, bg='black')
        canvas.place(x=0, y=26)
        frame.pack()

    def get_order_dict(self, event=None):
        """Функция проверки корректности введеного номера заказа и получение его значения из БД"""
        order_name = self.order_name_entry_var.get()
        self.order_exist = None
        if re.fullmatch(r'\d{6}', order_name):
            for day_dict in Conf.read_pcl_log_for_processing():
                if order_name in day_dict:
                    self.order_exist = {'PATH': day_dict['PATH'], 'NAME': order_name, 'CONTENTS': day_dict[order_name]}
                    break
        if self.order_exist:
            self.order_name_label.config(text=f'Обработка заказа: {order_name}')
        else:
            self.order_name_label.config(text='Для запуска обработчика введите номер заказа')
        self.order_name_entry_var.set('')
        self.reset_settings_to_default()

    def buttons_frame(self):
        """Функция отрисовки основных кнопок"""
        frame = tk.Frame(master=self, width=300, height=33)
        canvas = tk.Canvas(master=frame, width=296, height=1, bg='black')
        canvas.place(x=0, y=0)
        run_button = tk.Button(master=frame, **self.style, text='Запустить', padx=5, command=self.init_proc)
        run_button.place(x=1, y=5)
        close_button = tk.Button(master=frame, **self.style, text='Выход', command=self.stop_func, padx=5)
        close_button.place(x=245, y=5)
        frame.pack()

    def stop_func(self):
        """Функция остановки процесса обработки"""
        try:
            self.destroy()
        except:
            pass

    def show_progress_widget(self):
        """Функция отрисовки виджетов прогресс бара и текстовых виджетов"""
        for name in self.winfo_children():
            name.destroy()
        self.geometry('300x105')
        self.to_parent_center()
        self.processing_info = ttk.Label(self,
                                         text='Номер заказа\nКоличество и название тиража\nНомер и название файла')
        self.processing_info.place(x=1, y=1)
        self.processing_pb = ttk.Progressbar(self, mode="determinate", length=296)
        self.processing_pb.place(x=1, y=51)
        self.close_button = tk.Button(self, text='Остановить', **self.style, command=self.stop_func)
        self.close_button.place(x=221, y=75)

    def init_proc(self, event=None):
        """Инициализация обработки с выводом информации на экран"""
        if not self.order_exist or not self.event_flag:
            return
        self.event_flag = False
        self.get_order_settings()
        self.show_progress_widget()
        self.processing_info.config(text='Формирую задачу')
        order_obj = None
        if type(self) == BackUpWindow:
            order_obj = FileProc.OrderBuckup(self.order_exist)
        if type(self) == SmartProcWindow:
            if not self.order_exist['CONTENTS']:
                self.destroy()
                return
            order_obj = FileProc.OrderSmartProcessor(self.order_exist)
        order_obj.get_file_list()
        total_count = order_obj.get_file_len()
        counter = 0
        self.processing_pb['maximum'] = total_count
        self.processing_pb['value'] = 0
        self.processing_info.config(text='Создаю каталоги')
        order_obj.make_dirs()
        self.update()
        for order, content, file in order_obj.processing_run():
            counter += 1
            self.processing_pb['value'] += 1
            self.processing_info.config(text=f'{order}\n{content}\n{total_count}/{counter} -- {file}')
            self.update()
        self.destroy()


class SmartProcWindow(ProcessingWindow):
    def __init__(self, parent_root):
        self.settings_dict = {}
        super().__init__(parent_root)
        self.grab_set()
        self.wait_window()

    def type_line_widget(self, book_type, text, frame_height, check_option):
        """Конструктор для полей, которые отображают тип обработки"""
        self.settings_dict[book_type] = {}
        frame = tk.Frame(master=self, width=300, height=frame_height)
        label = ttk.Label(master=frame, text=text)
        label.place(x=0, y=0)
        combobox = ttk.Combobox(frame, width=45, state="readonly")
        combobox.place(x=4, y=20)
        coords = ((20, 41), (150, 41), (20, 61), (150, 61), (20, 81))
        self.settings_dict[book_type].update({'label': label})
        self.settings_dict[book_type].update({'combobox': combobox})
        if check_option:
            self.settings_dict[book_type]['checkbutton'] = {}
            for i, v in enumerate(check_option):
                pos_x, pos_y = coords[i]
                var, rus_text = v
                frame.__dict__[var] = tk.BooleanVar(frame)
                frame.__dict__[var].set(False)
                check_btn = ttk.Checkbutton(frame, text=rus_text, variable=frame.__dict__[var])
                check_btn.place(x=pos_x, y=pos_y)
                self.settings_dict[book_type]['checkbutton'].update({var: (check_btn, frame.__dict__[var])})
        frame.pack()

    def show_undetected_edition_frame(self):
        """Отрисовка фрейма нераспознанных тиражей"""
        self.settings_dict['undetected'] = {}
        label = ttk.Label(self, text='Список нераспознанных тиражей')
        label.pack()
        combobox = ttk.Combobox(self, width=45)
        combobox.pack()
        self.settings_dict['undetected'].update({'label': label, 'combobox': combobox})

    def disable_info_widgets(self):
        """Перевод всех фреймов в неактивное положение"""
        for vals in self.settings_dict.values():
            vals['label'].config(state=tk.DISABLED)
            vals['combobox'].config(state=tk.DISABLED)
            vals['combobox'].set('')
            cbuns = vals.get('checkbutton', '')
            if cbuns:
                for widget, var in cbuns.values():
                    widget.config(state=tk.DISABLED)
                    var.set(False)

    def enable_info_widgets(self, order_dct):
        """Перевод фреймов в активное положение, согласно типам продукта в заказе"""
        for key, value in order_dct.items():
            widgets = self.settings_dict[key]
            widgets['label'].config(state=tk.NORMAL)
            widgets['combobox'].config(state='readonly', values=value)
            cbuns = widgets.get('checkbutton', '')
            if cbuns:
                for name, tup in cbuns.items():
                    tup[0].config(state=tk.NORMAL)
                    if key == 'photobook' and name in ('stroke', 'guideline', 'generate .mrk'):
                        tup[1].set(True)
                    if key == 'layflat' and name == 'guideline':
                        tup[1].set(True)
                    if key == 'album':
                        tup[1].set(True)

    def show_main_frame(self):
        """Отрисовка основных виджетов"""
        self.type_line_widget('photobook', 'Книги на Фотобумаге -- Раскидывание по каналам', 100,
                              (('stroke', 'Обводка'), ('rename', 'Переименование'), ('guideline', 'Направляющие'),
                               ('add backprint', 'Добавить Бек-Принт'), ('generate .mrk', 'Сформировать .mrk')))
        self.type_line_widget('layflat', "Layflat'ы -- Извлечение Спец-Папок", 61,
                              (('guideline', 'Направляющие'), ('rename', 'Переименование')))
        self.type_line_widget('album', "Альбомы, PUR, FlexBind'ы -- Раскодировка", 61,
                              (('guideline', 'Направляющие'), ('rename', 'Переименование')))
        self.type_line_widget('journal', 'Журналы -- Раскодировка', 41, None)
        self.type_line_widget('photocanvas', 'Холсты -- Подготовка к печати', 41, None)
        self.show_undetected_edition_frame()
        self.disable_info_widgets()

    def get_order_dict(self, event=None):
        super().get_order_dict()
        self.disable_info_widgets()
        if not self.order_exist:
            return
        book_dict = {}
        for name, values in self.order_exist['CONTENTS'].items():
            book_type = values[1]
            if book_type == 'PHOTO':
                continue
            if book_type is None:
                book_dict.setdefault('undetected', []).append(name)
            if book_type:
                lib_cat = self.parent_root.LIBRARY[book_type]['category']
                if lib_cat in ('photobook', 'layflat', 'journal', 'album', 'photocanvas'):
                    book_dict.setdefault(lib_cat, []).append(name)
        self.enable_info_widgets(book_dict)

    def get_order_settings(self):
        edition_to_print = {}
        processing_settings = {}
        for key, value in self.order_exist.pop('CONTENTS').items():
            if value[1] is None or value[1] == 'PHOTO':
                continue
            lib = self.parent_root.LIBRARY[value[1]].copy()
            lib_cat = lib['category']
            if lib_cat in ('photobook', 'layflat', 'journal', 'album', 'photocanvas'):
                edition_to_print[key] = lib
                edition_to_print[key].update({'combination': value[0][-1]})
            if lib_cat in ('photobook', 'layflat', 'album'):
                stg = {k: v[1].get() for k, v in self.settings_dict[lib_cat]['checkbutton'].items()}
                common = ('stroke_size', 'stroke_color', 'guideline_size', 'guideline_color')
                stg.update({k: self.parent_root.SETTINGS[k] for k in common})
                processing_settings[lib_cat] = stg
        self.order_exist['CONTENTS'] = edition_to_print
        self.order_exist['PROC_STG'] = processing_settings


class BackUpWindow(ProcessingWindow):
    def __init__(self, parent_root):
        self.order_list_radio = None
        self.order_list_cb = None
        self.order_type_radio = None
        super().__init__(parent_root)
        self.grab_set()
        self.wait_window()

    def init_local_variables(self):
        self.order_list_radio = tk.StringVar(self)
        self.order_type_radio = tk.StringVar(self)
        self.reset_settings_to_default()

    def show_main_frame(self):
        frame = tk.Frame(self, width=300, height=75)
        order_list_radio1 = ttk.Radiobutton(master=frame, text='Бакапнуть все', command=self.order_list_radio_switcher,
                                            value='ALL', variable=self.order_list_radio)
        order_list_radio1.place(x=1, y=2)
        order_list_radio2 = ttk.Radiobutton(master=frame, text='Выбранный тираж',
                                            command=self.order_list_radio_switcher,
                                            value='CHOSEN', variable=self.order_list_radio)
        order_list_radio2.place(x=155, y=2)
        self.order_list_cb = ttk.Combobox(master=frame, state=tk.DISABLED, width=46)
        self.order_list_cb.place(x=1, y=26)
        type_radio1 = ttk.Radiobutton(master=frame, text='Все файлы',
                                      value='ALL', variable=self.order_type_radio)
        type_radio1.place(x=1, y=51)
        type_radio2 = ttk.Radiobutton(master=frame, text='Спец-папки',
                                      value='CCV', variable=self.order_type_radio)
        type_radio2.place(x=108, y=51)
        type_radio3 = ttk.Radiobutton(master=frame, text='Экзепляры',
                                      value='EX', variable=self.order_type_radio)
        type_radio3.place(x=216, y=51)
        frame.pack()

    def reset_settings_to_default(self):
        self.order_list_radio.set('ALL')
        self.order_type_radio.set('CCV')
        if self.order_list_cb:
            self.order_list_cb.config(state=tk.DISABLED)

    def order_list_radio_switcher(self):
        order_list = self.order_list_radio.get()
        if order_list == 'ALL':
            self.order_list_cb.config(state=tk.DISABLED)
        if order_list == 'CHOSEN':
            if self.order_exist:
                self.order_list_cb.config(values=tuple(self.order_exist['CONTENTS'].keys()))
            self.order_list_cb.config(state="readonly")

    def get_order_settings(self):
        if self.order_list_radio.get() == 'CHOSEN':
            chosen_order = self.order_list_cb.get()
            if chosen_order:
                self.order_exist['CONTENTS'] = {chosen_order: self.order_exist['CONTENTS'][chosen_order]}
        self.order_exist.update({'TYPE': self.order_type_radio.get()})


class InformationWindow(ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.main_settings()
        self.dates_list = tuple(x[:-4] for x in Conf.get_logs_list())
        self.combo1 = None
        self.combo2 = None
        self.tree = None
        self.show_main_frame()
        self.to_parent_center()

    def main_settings(self):
        self.title('Информация по продуктам')
        self.resizable(False, False)

    def show_main_frame(self):
        label = ttk.Label(self, text='Укажите период для подсчета')
        label.pack()
        self.dates_ask_frame()
        frame = tk.Frame(self)
        frame.pack(expand=1, fill=tk.BOTH)
        self.tree = ttk.Treeview(frame, show='tree', height=20)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=2)
        scrollbar = ttk.Scrollbar(master=frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        export_btn = tk.Button(self, text='Экспортировать', **self.style)
        export_btn.pack(side=tk.LEFT, padx=4, pady=4)
        close_btn = tk.Button(self, text='Закрыть', **self.style, command=self.destroy)
        close_btn.pack(side=tk.RIGHT, padx=4, pady=4)

    def dates_ask_frame(self):
        frame = tk.Frame(self)
        label1 = ttk.Label(frame, text='С:')
        label1.grid(row=0, column=0)
        self.combo1 = ttk.Combobox(frame, state='readonly', values=self.dates_list)
        self.combo1.grid(row=0, column=1)
        label2 = ttk.Label(frame, text='По:')
        label2.grid(row=0, column=2)
        self.combo2 = ttk.Combobox(frame, state='readonly', values=self.dates_list)
        self.combo2.grid(row=0, column=3)
        init_btn = tk.Button(frame, text='Посчитать', **self.style, command=self.init_counter)
        init_btn.grid(row=0, column=4, padx=10)
        frame.pack(pady=4, padx=2)

    def clear_tree(self):
        for i in self.tree.get_children(''):
            self.tree.delete(i)

    def init_counter(self):
        date1, date2 = self.combo1.get(), self.combo2.get()
        if not date1 or not date2:
            return
        self.combo1.set('')
        self.combo2.set('')
        counter_obj = Inf.ProductInfo(Conf.read_chosen_pcl_log(*sorted((date1, date2))), self.parent_root.LIBRARY)
        books, photos, undetected = counter_obj.get_info()
        self.clear_tree()
        if books:
            self.__init_category(books)
            self.__init_sub_category(books)
            self.__init_product(books)
        if photos:
            self.tree.insert('', tk.END, iid=4, text='Химическая фотопечать')
            for string in sorted(f'{k} -- {v}шт' for k, v in photos.items()):
                self.tree.insert(4, index=tk.END, text=string)
        if undetected:
            self.tree.insert('', tk.END, iid=5, text='Нераспознанные тиражи')
            for string in sorted(f'{k} -- {v}шт' for k, v in undetected.items()):
                self.tree.insert(5, index=tk.END, text=string)

    def __init_category(self, book_lst):
        premium, edition, mat_lst = False, False, True
        for product in book_lst:
            if product['category'] == 'Премиум':
                premium = True
            if product['category'] == 'Тираж':
                edition = True
        if premium:
            self.tree.insert('', tk.END, iid=1, text='Премиум')
        if edition:
            self.tree.insert('', tk.END, iid=2, text='Тиражи')
        self.tree.insert('', tk.END, iid=3, text='Сводный список материалов')

    def __init_sub_category(self, book_lst):
        premium = {'Книги': 0, 'Люксы': 0, 'Кожаные обложки': 0, 'FlexBind': 0, 'Холсты': 0, 'Остальное': 0}
        edition = {'Книги': 0, 'Планшеты': 0, 'Альбомы': 0, 'Дуо и Трио': 0,  'Остальное': 0}
        for product in book_lst:
            if product['category'] == 'Премиум':
                premium[product['sub_cat']] += product['pr_count']
            if product['category'] == 'Тираж':
                edition[product['sub_cat']] += product['pr_count']
        for ind, value in enumerate(premium.items()):
            sub, counter = value
            if counter > 0:
                self.tree.insert(1, iid=int(f'1{ind}'), index=tk.END, text=f'{sub} -- {counter}')
        for ind, value in enumerate(edition.items()):
            sub, counter = value
            if counter > 0:
                self.tree.insert(2, iid=int(f'2{ind}'), index=tk.END, text=f'{sub} -- {counter}')

    def __init_product(self, book_lst):
        premium_ind = ('Книги', 'Люксы', 'Кожаные обложки', 'FlexBind', 'Холсты', 'Остальное')
        edition_ind = ('Книги', 'Планшеты', 'Альбомы', 'Дуо и Трио', 'Остальное')
        premium_lst = {}
        edition_lst = {}
        main_mat_lst = {}
        for product in book_lst:
            if product['category'] == 'Премиум':
                premium_lst.setdefault(product['pr_name'], {'ind': 0, 'count': 0, 'mat_lst': {}})
                premium_lst[product['pr_name']]['ind'] = int(f'1{premium_ind.index(product["sub_cat"])}')
                premium_lst[product['pr_name']]['count'] += product['pr_count']
                for k, v in product['mat_lst'].items():
                    premium_lst[product['pr_name']]['mat_lst'].setdefault(k, 0)
                    premium_lst[product['pr_name']]['mat_lst'][k] += v
                    main_mat_lst.setdefault(k, 0)
                    main_mat_lst[k] += v
            if product['category'] == 'Тираж':
                edition_lst.setdefault(product['pr_name'], {'ind': 0, 'count': 0, 'mat_lst': {}})
                edition_lst[product['pr_name']]['ind'] = int(f'2{edition_ind.index(product["sub_cat"])}')
                edition_lst[product['pr_name']]['count'] += product['pr_count']
                for k, v in product['mat_lst'].items():
                    edition_lst[product['pr_name']]['mat_lst'].setdefault(k, 0)
                    edition_lst[product['pr_name']]['mat_lst'][k] += v
                    main_mat_lst.setdefault(k, 0)
                    main_mat_lst[k] += v
        for i, v in enumerate(sorted(premium_lst.items())):
            name, values = v
            ind = int(f'{values["ind"]}{i}')
            self.tree.insert(values['ind'], iid=ind, index=tk.END, text=f'{name} -- {values["count"]}')
            for x, y in sorted(values['mat_lst'].items()):
                self.tree.insert(ind, index=tk.END, text=f'{x} -- {y}')
        for i, v in enumerate(sorted(edition_lst.items())):
            name, values = v
            ind = int(f'{values["ind"]}{i}')
            self.tree.insert(values['ind'], iid=ind, index=tk.END, text=f'{name} -- {values["count"]}')
            for x, y in sorted(values['mat_lst'].items()):
                self.tree.insert(ind, index=tk.END, text=f'{x} -- {y}')
        for k, v in sorted(main_mat_lst.items(), key=lambda x: x[1], reverse=True):
            self.tree.insert(3, index=tk.END, text=f'{k} -- {v}')


class MailSamplesWindow(ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Текстовые шаблоны')
        self.mail_samples = MailSamples()
        self.listbox = None
        self.listbox_values = tk.Variable(self, value=self.mail_samples.get_ms_list())
        self.main()

    def main(self):
        self.show_listbox_widget()
        self.show_buttons_widgets()
        self.to_parent_center()
        self.resizable(False, False)
        self.focus()

    def show_listbox_widget(self):
        """Функция отрисовки виджета ListBox с прокрутокой содержимого"""
        frame = tk.Frame(self)
        self.listbox = tk.Listbox(frame, width=50, listvariable=self.listbox_values)
        self.listbox.pack(side=tk.LEFT)
        self.listbox.bind("<Return>", self.init_sample)
        scrollbar = ttk.Scrollbar(master=frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscroll=scrollbar.set)
        frame.pack()

    def show_buttons_widgets(self):
        """Функция отрисовки кнопок взаимодействия"""
        init_btn = tk.Button(self, text='Использовать', **self.style, command=self.init_sample)
        init_btn.pack(side=tk.LEFT, padx=2, pady=2)
        close_btn = tk.Button(self, text='Закрыть', **self.style, command=self.destroy)
        close_btn.pack(side=tk.RIGHT, padx=2, pady=2)

    def init_sample(self, event=None):
        """Копирование шаблона в буфер обмена. Если нет литералов - копируется сразу, если есть, то появляется
        окно-помошник для заполнения пропусков"""
        index = self.listbox.curselection()
        if not index:
            return
        self.mail_samples.create_sample(index[0])
        if len(self.mail_samples.SAMPLE) == 1:
            string = self.mail_samples.SAMPLE[0]
        else:
            AssistWindow(self)
            string = ''.join(self.mail_samples.SAMPLE)
        self.clipboard_clear()
        self.clipboard_append(string)
        tkmb.showinfo(title='Текстовый шаблон', message='Текстовый шаблон скопирован в буфер обмена')
        self.focus()


class AssistWindow(ChildWindow):
    """Вспомогательный класс, который вызывается когда в текстовом шаблоне присутствуют переменные значения"""
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.widget_lst = []
        self.mail_samples = MailSamples()
        self.main()
        self.bind("<Return>", self.create_string)
        self.focus()

    def main(self):
        self.overrideredirect(True)
        self.config(border=1, relief='solid')
        label = ttk.Label(self, text='Заполните поля:')
        label.pack()
        self.show_entry_widget()
        enter_btn = tk.Button(self, text='Ввод', **self.style, command=self.create_string, width=10)
        enter_btn.pack(padx=2, pady=2)
        self.to_parent_center()

    def show_entry_widget(self):
        """Функция отрисовки Entry виджетов для ввода информации в шаблон"""
        for variable in self.mail_samples.SAMPLE[1::2]:
            label = ttk.Label(self, text=variable)
            label.pack(anchor=tk.NW)
            entry = ttk.Entry(self, width=30)
            entry.pack(padx=2)
            self.widget_lst.append(entry)

    def create_string(self, event=None):
        """Функция для сбора шаблона из введенных значений"""
        for i in range(1, len(self.mail_samples.SAMPLE), 2):
            self.mail_samples.SAMPLE[i] = self.widget_lst[i // 2].get()
        self.destroy()


class MailSamples:
    """Класс для обработки файлов текстовых шаблонов"""
    __slots__ = '__ms_list'
    __INSTANCE = None
    SAMPLE = []

    def __new__(cls, *args, **kwargs):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(self):
        self.__ms_list = tuple(x for x in os.listdir('data/MailSamples') if x != '__readme.txt')

    def get_ms_list(self) -> tuple:
        """Возвращает кортеж из значенией списка текстовых шаблонов"""
        return tuple(x[:-4] for x in self.__ms_list)

    def create_sample(self, index: int):
        """Разбивает строки на части по литералу ?%"""
        with open(f'data/MailSamples/{self.__ms_list[index]}', 'r', encoding='UTF-8') as txt_file:
            self.SAMPLE.clear()
            self.SAMPLE.extend(txt_file.read().split('?%'))
