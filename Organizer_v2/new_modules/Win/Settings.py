import new_modules.Win.Source as Source


class SettingsWindow(Source.ChildWindow):
    """Окно основных настроек приложения"""
    def __init__(self, main_window):
        super().__init__(main_window)
        self.__main()

    def __main(self):
        self.title('Настройки')
        self.show_autolog_widget()
        self.geometry('260x336')
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
            autolog = self.parent_root.app_settings.read('autolog')
            autolog_label.config(text='Автолог: Активен' if autolog else 'Автолог: Отключен')
            autolog_init_bt.config(text='Отключить' if autolog else 'Включить')

        def init_autolog():
            Source.tkmb.showinfo('Автолог', 'Функция автолога отключена.\nПожалуйста, обновляйте лог вручную.')

        frame = Source.tk.Frame(self)
        autolog_label = Source.ttk.Label(frame)
        autolog_label.pack(side=Source.tk.LEFT, pady=2, padx=2)
        autolog_init_bt = Source.MyButton(frame, command=init_autolog, width=12)
        autolog_init_bt.pack(side=Source.tk.RIGHT, padx=2, pady=2)
        update_label_info()
        frame.pack(fill=Source.tk.X)

    def show_log_check_depth_widget(self):
        """Функция отрисовки виджета управления глубиной проверки заказов"""
        def update_text_value():
            label.config(text=f'Глубина проверки лога - {self.parent_root.app_settings.read("log_check_depth")} заказов')

        def update_depth_value():
            value = entry_var.get()
            if value.isdigit():
                self.parent_root.app_settings.update(log_check_depth=int(value))
            update_text_value()
            entry.delete(0, Source.tk.END)

        separator = Source.tk.Canvas(self, height=1, bg='black')
        separator.pack(fill=Source.tk.X)
        frame = Source.tk.Frame(self)
        label = Source.ttk.Label(frame)
        label.pack(anchor=Source.tk.NW, padx=2)
        update_text_value()
        entry_var = Source.tk.StringVar(frame)
        entry = Source.ttk.Entry(frame, width=10, textvariable=entry_var)
        entry.pack(side=Source.tk.LEFT, padx=4)
        update_button = Source.MyButton(frame, text='Задать', command=update_depth_value, width=12)
        update_button.pack(side=Source.tk.RIGHT, padx=2)
        frame.pack(fill=Source.tk.X)

    def show_cover_proc_settings(self, color_text, color_stg_key, size_text, size_stg_key):
        """Функция-конструктор для управления цветом и толщиной для направляющих и обводки"""
        def update_color():
            color = Source.tkcc.askcolor()
            if color:
                self.parent_root.app_settings.update(**{color_stg_key: color[1]})
                color_btn.config(bg=color[1])

        def update_size_label():
            size_label.config(text=f'{size_text}: {self.parent_root.app_settings.read(size_stg_key)} пикселей')

        def update_size(val):
            if int(val) != self.parent_root.app_settings.read(size_stg_key):
                self.parent_root.app_settings.update(**{size_stg_key: int(val)})
                update_size_label()

        separator = Source.tk.Canvas(self, height=1, bg='black')
        separator.pack(fill=Source.tk.X)
        frame = Source.tk.Frame(self)
        label = Source.ttk.Label(frame, text=color_text)
        label.pack(side=Source.tk.LEFT, padx=2)
        color_btn = Source.tk.Button(frame, relief=Source.tk.FLAT, width=12, command=update_color,
                                     bg=self.parent_root.app_settings.read(color_stg_key))
        color_btn.pack(side=Source.tk.RIGHT, padx=2)
        frame.pack(fill=Source.tk.X)
        size_label = Source.tk.Label(self)
        size_label.pack(anchor=Source.tk.NW)
        update_size_label()
        scale = Source.tk.Scale(self, orient=Source.tk.HORIZONTAL, from_=1, to=10, length=255, showvalue=False,
                                command=update_size)
        scale.pack()
        scale.set(self.parent_root.app_settings.read(size_stg_key))

    def show_directory_widget(self, text, settings_key):
        """Функция-конструктор для управления основными дирректориями"""
        def update_directory():
            path = Source.tkfd.askdirectory()
            if path:
                text_var.set(path)
                self.parent_root.app_settings.update(**{settings_key: path})

        separator = Source.tk.Canvas(self, height=1, bg='black')
        separator.pack(fill=Source.tk.X)
        text_var = Source.tk.StringVar(self, value=self.parent_root.app_settings.read(settings_key))
        dir_status_label = Source.tk.Label(self, text=text)
        dir_status_label.pack(anchor=Source.tk.NW)
        dir_update_button = Source.MyButton(self, textvariable=text_var, command=update_directory)
        dir_update_button.pack(fill=Source.tk.X, padx=2)
