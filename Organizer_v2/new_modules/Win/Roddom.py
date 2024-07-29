import new_modules.Win.Source as Source
from new_modules.Roddom import RoddomOrder


class RoddomWindow(Source.ChildWindow):
    """Окно Роддома"""

    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.order_exist = None         # Переменные, которые используют виджеты
        self.directory_info = Source.tk.StringVar(self, self.parent_root.app_settings.read('roddom_main_dir'))
        self.order_calc_info = None
        self.text_res_enable = Source.tk.BooleanVar(self, value=True)
        self.disabled_widget = []
        self.__main()

    def __main(self):
        self.title('Роддом')
        self.geometry('260x217')
        self.resizable(False, False)
        self.show_directory_widget()
        self.info_frame = Source.tk.Frame(self, width=260, height=80)
        self.info_frame.pack()
        self.show_cb_frame()
        self.show_buttons_widget()
        self.to_parent_center()
        self.focus()

    def show_directory_widget(self):
        """Функция отрисовки фрейма с информацией, где храняться заказы роддома"""
        dir_status_label = Source.ttk.Label(self, text='Папка, куда сохраняются заказы Роддом\'а')
        dir_status_label.pack(anchor=Source.tk.NW, padx=2, pady=2)
        dir_update_button = Source.MyButton(self, textvariable=self.directory_info, command=self.update_directory)
        dir_update_button.pack(padx=2, fill=Source.tk.X)
        self.disabled_widget.append(dir_update_button)
        separator = Source.tk.Canvas(self, height=1, bg='black')
        separator.pack()

    def update_directory(self):
        """Функция смены папки размещения заказов роддома"""
        new_path = Source.tkfd.askdirectory()
        if new_path:
            self.directory_info.set(new_path)
            self.parent_root.app_settings.update(roddom_main_dir=new_path)

    def show_cb_frame(self):
        """Функция отрисовки Checkbutton - настроек обработки заказов роддома"""
        separator = Source.tk.Canvas(self, height=1, bg='black')
        separator.pack()
        text_res_cb = Source.ttk.Checkbutton(self, text='Сохранять результаты в sum.txt', variable=self.text_res_enable)
        text_res_cb.pack(anchor=Source.tk.NW, padx=2)
        self.disabled_widget.append(text_res_cb)

    def show_buttons_widget(self):
        """Функция отрисовки кнопок, для взаимодействия с заказом"""
        button1 = Source.MyButton(self, text='Посчитать заказ', command=self.init_calc, width=15)
        button1.pack(anchor=Source.tk.NW, padx=2)
        button2 = Source.MyButton(self, text='Скопировать инф', command=self.info_to_clipboard, width=15)
        button2.pack(side=Source.tk.LEFT, padx=2, pady=2)
        button3 = Source.MyButton(self, text='Отправить в печать', command=self.to_print)
        button3.pack(side=Source.tk.RIGHT, padx=2, pady=2)
        self.disabled_widget.extend([button1, button3])

    def init_calc(self):
        """Функция вызова метода подсчета из заказа - объекта Роддома"""
        order = Source.tkfd.askdirectory(initialdir=self.directory_info.get())
        if not order:
            return
        self.order_exist = RoddomOrder(order, self.text_res_enable.get())
        self.order_calc_info = str(self.order_exist)
        self.show_order_info(self.order_calc_info)
        self.info_to_clipboard()

    def info_to_clipboard(self):
        """Функция, которая заносит информацию о пути и дате заказа в будфер обмена"""
        Source.tk.Tk.clipboard_clear(self)
        Source.tk.Tk.clipboard_append(self, self.order_calc_info)

    def info_frame_clear(self):
        """Функция очистки info_frame"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()

    def show_order_info(self, text):
        """Функция отрисовки подсчитанной информации"""
        self.info_frame_clear()
        label = Source.ttk.Label(self.info_frame, text=text, font=12)
        label.place(x=0, y=0)

    def button_disabler(self):
        """Функция, которая выключает взаимодействие с кнопками"""
        for widget in self.disabled_widget:
            widget.config(state="disabled")

    def button_enabler(self):
        """Функция, которая включает взаимодействие с кнопками"""
        for widget in self.disabled_widget:
            widget.config(state="normal")

    @Source.safe_close
    def to_print(self):
        """Функция отправки в печать. Отображает на экране информацию о коопировани и вызывает методы копирования"""
        path = Source.tkfd.askdirectory(initialdir=self.parent_root.app_settings.read('fotoprint_temp_dir'))
        if not path or not self.order_exist:
            return
        self.order_calc_info = f'{path}\n\nРоддом\n\n{self.order_exist.order_name}'
        self.info_to_clipboard()
        self.info_frame_clear()
        self.button_disabler()
        operation_label = Source.tk.Label(self.info_frame, text='Создаю Каталоги')
        operation_label.place(x=0, y=0)
        file_label = Source.tk.Label(self.info_frame, text='Вторая строчка')
        file_label.place(x=0, y=15)
        progressbar = Source.ttk.Progressbar(self.info_frame, orient=Source.tk.HORIZONTAL, mode="determinate",
                                             length=254)
        progressbar.place(x=3, y=40)
        self.order_exist.create_directory(path)
        progressbar['maximum'] = sum(self.order_exist.total_sum.values())
        progressbar['value'] = 0
        operation_label.config(text='Копирую файлы')
        for name in self.order_exist.run(path):
            progressbar['value'] += 1
            file_label.config(text=f'{progressbar["value"]}/{progressbar["maximum"]} -- {name}')
            self.update()
        operation_label.config(text='Завершено')
        file_label.config(text='')
        self.button_enabler()
        self.order_exist = None
