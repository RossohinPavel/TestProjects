from ...source import *
from ...source.style import style_init
from .library import LibraryWindow
from modules.utilits.telebot import bot as tele_bot


class SettingsFrame(ttk.Frame):
    """Фрейм основных настроек приложения"""

    def __init__(self, master: Any):
        super().__init__(master, padding=5)
        self.dark_menu = self.light_menu = None
        self.init_color_menus()
        self.draw_theme_widgets()
        self.draw_library_widgets()
        self.draw_directory_widgets()
        self.draw_telegrambot_frame()

    def theme_closure(self, name: str) -> Callable:
        """Замыкание для смены тем"""
        return lambda: setattr(APP.stg, 'color', name)

    def init_color_menus(self) -> None:
        dark = ('solar', 'superhero', 'darkly', 'cyborg', 'vapor')
        light = (
            'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 
            'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean'
        )

        self.dark_menu = ttk.Menu(self)
        for name in dark:
            self.dark_menu.add_command(
                label=f'  {name}'.ljust(29, ' '),
                command=self.theme_closure(name)
            )
        self.light_menu = ttk.Menu(self)
        for name in light:
            self.light_menu.add_command(
                label=f'  {name}'.ljust(29, ' '),
                command=self.theme_closure(name)
            )
    
    def draw_theme_widgets(self) -> None:
        HeaderLabel(self, 'Оформление').pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 2))

        container = ttk.Frame(self, padding=(5, 0, 5, 15))
        container.pack(fill=ttkc.X)

        # Свитчер тем
        theme_frame = ttk.Frame(container, height=44)
        theme_frame.pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(0, 3))

        HeaderLabel(theme_frame, text='Тема', anchor='n').place(x=0, y=0, relwidth=1)

        theme_menu = ttk.Menu(theme_frame)
        theme_menu.add_command(
            label='  light', 
            command=lambda: setattr(APP.stg, 'theme', 'light')
        )
        theme_menu.add_command(
            label='  dark', 
            command=lambda: setattr(APP.stg, 'theme', 'dark')
            )
        theme_btn = ttk.Menubutton(theme_frame, menu=theme_menu, style='outline', padding=(5, 2, 2, 2))
        theme_btn.place(x=0, y=15, relwidth=1)

        # Добавление вызова в Дескриптор тем
        APP.desc.theme.add_call(lambda v: theme_btn.configure(text=v))      #type: ignore

        # Свитчер палитр
        palette_frame = ttk.Frame(container, height=44)
        palette_frame.pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 3))
        ttk.Frame(container, height=44).pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 0))

        HeaderLabel(palette_frame, text='Палитра', anchor='n').place(x=0, y=0, relwidth=1)

        def theme_switch(theme: str) -> None:
            """Переключает тему в меню"""
            menu = self.dark_menu
            if theme == 'light':
                menu = self.light_menu
            palette_btn.configure(menu=menu)    #type: ignore
            if APP.desc.color._value:    #type: ignore
                menu.invoke(0)                  #type: ignore

        palette_btn = ttk.Menubutton(palette_frame, style='outline', padding=(5, 2, 2, 2))
        palette_btn.place(x=0, y=15, relwidth=1)

        # Добавление вызова в Дескриптор тем и палитр
        APP.desc.theme.add_call(theme_switch)                               #type: ignore
        APP.desc.color.add_call(lambda v: palette_btn.configure(text=v))    #type: ignore
        APP.desc.color.add_call(lambda v: style_init(v))                    #type: ignore

    def draw_library_widgets(self) -> None:
        """Отрисовка виджетов библиотеки"""
        hl = HeaderLabel(self, 'Настройка библиотеки')
        hl.pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 2))

        container = ttk.Frame(self, padding=(5, 0, 5, 15))
        container.pack(fill=ttkc.X)

        # Фреймы существуют для выравнивания полжения кнопок, 
        # т.к размер кнопки зависит от длинны текста
        frame = ttk.Frame(container, height=25)
        frame.pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(0, 3))
        ttk.Frame(container, height=25).pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 3))
        ttk.Frame(container, height=25).pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 0))

        btn = ttk.Button(
            frame, 
            padding=2, 
            text='Библиотека', 
            command=lambda: LibraryWindow()
        )
        btn.place(x=0, y=0, relwidth=1)

    def draw_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        self.draw_directory_frame('Диск загрузки заказов \'Z\'', 'z_disc')
        self.draw_directory_frame('Диск печати заказов \'О\'', 'o_disc')
        self.draw_directory_frame('Диск операторов фотопечати \'Т\'', 't_disc')

    def draw_directory_frame(self, text: str, attr: str) -> None:
        """Отрисовка виджетов управления рабочими папками"""
        HeaderLabel(self, text).pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 3))
        btn = SettingLine(self, lambda: self._update_dir(attr))
        btn.pack(padx=5, pady=(0, 15), anchor=ttkc.W)

        # Добавление вызова дескриптору
        add_call_func = eval(f'APP.desc.{attr}.add_call')
        add_call_func(lambda e: btn.var.set(e))

    def _update_dir(self, attr: str) -> None:
        """Получение информации из файлового диалога"""
        path = tkfd.askdirectory(
            parent=APP.mw, 
            initialdir=getattr(APP.stg, attr), 
            title=f'Выберите расположение'
        )
        if path:
            setattr(APP.stg, attr, path)
    
    def draw_telegrambot_frame(self) -> None:
        """Отриосвка фрейма телеграм помошника"""
        l = HeaderLabel(self, 'Телеграм-Помощник')
        l.pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 3))

        var = ttk.IntVar(self, value=0)
        btn = ttk.Checkbutton(
            self,
            offvalue=0,
            onvalue=1,
            style='success-round-toggle',
            variable=var
        )
        btn.configure(command=self.cmd_init_telebot(var, btn))
        btn.pack(padx=5, anchor=ttkc.W)
    
    def cmd_init_telebot(self, var: ttk.IntVar, btn: ttk.Checkbutton):
        """Замыкание, для запуска телебота и изменения статуса кнопки."""
        change_status = lambda: btn.configure(text='Активен' if var.get() else 'Неактивен')       
        change_status()
        
        def closure():
            if var.get():
                token = Querybox.get_string(
                    prompt='Введите токен для активации бота',
                    title='Телеграм-Помощник'
                )
                if token:
                    tele_bot.main(token)
                    change_status()
                else:
                    var.set(0)
            else:
                tele_bot.main('stop')
                change_status()

        return closure
