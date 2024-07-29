from .source import *
from .source.style import style_init
from .source.menu_button import MenuButton
from . import frames


class MainWindow(ttk.Window):
    """Основное окно приложения"""

    def __init__(self) -> None:
        super().__init__(title='Органайзер 3.11.5 BETA', iconphoto='data/assets/ico.png')
        # Запускаем определение стилей и получения изображений после __init__
        style_init()
        self.init_images()
        self.set_main_graph_settings()

        # Отрисовываем колонку меню
        menu_column = ttk.Frame(self)
        menu_column.pack(side=ttkc.LEFT, fill=ttkc.Y)

        self.todo = MenuButton('TODO', menu_column, frames.TODOFrame)
        self.todo.pack(anchor=ttkc.N)

        self.social = MenuButton('SOCIAL', menu_column, frames.MailSamplesFrame,)
        self.social.pack(anchor=ttkc.N)

        self.info = MenuButton('INFO', menu_column, frames.InfoFrame)
        self.info.pack(anchor=ttkc.N)

        self.file = MenuButton('FILE', menu_column, frames.FileFrame)
        self.file.pack(anchor=ttkc.N)

        self.stg = MenuButton('SETTINGS', menu_column, frames.SettingsFrame)
        self.stg.pack(anchor=ttkc.S, expand=1, pady=(0, 5))

        # Бинды на переключение "страничек" приложения по нажатию
        # комбинаций клавиш Ctrl + 1, и так далее.
        for i, widget in enumerate((self.todo, self.social, self.info, self.file), 1):
            self.bind(f'<Control-KeyPress-{i}>', widget.click)

        # Разделитель
        ttk.Separator(self, orient='vertical').pack(side=ttkc.LEFT, fill=ttkc.Y, pady=5)

        # Запускаем 1 фрейм - Лист задач
        self.todo.click(None)
    
    def init_images(self) -> None:
        """Ф-я, загружающая изображения."""
        from .source import images
        for k, v in images.__dict__.items():
            if not k.startswith('__'):
                setattr(images, k, ttk.PhotoImage(master=self, file=v))

    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        width, height = 550, 350
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.event_add('<<New>>', '<Control-n>')
        self.event_add('<<Save>>', '<Control-s>')
        self.bind_all('<Control-Key>', self.russian_hotkeys)
        self.update_idletasks()

    @staticmethod
    def russian_hotkeys(event: tkinter.Event):
        """Генерирует эвент согласно нажатым клавишам на русской раскладке клавиатуры."""
        if event.keysym != '??': return
        
        match event.keycode:
            case 67: venv = '<<Copy>>'
            case 78: venv = '<<New>>'
            case 83: venv = '<<Save>>'
            case 86: venv = '<<Paste>>'
            case 88: venv = '<<Cut>>'
            case 90: venv = '<<Undo>>'
            case _: venv = None
        
        if venv: event.widget.event_generate(venv)

    def destroy(self) -> None:
        """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
        ttl = 'Очередь задач не пуста'
        msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
        if APP.queue.value > 0:
            if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
                return
        super().destroy()
