from .main import ttk, Any
from ... import app_manager


class ChildWindow(ttk.Toplevel):
    """Конструктор для дочерних окон"""
    width = 100
    height = 100

    # Переменная для хранения имени окна
    win_title = None

    # Список обязательных атирбутов для инициализации ttk.Toplevel
    __TK_KWARGS = (
        'title', 
        'iconphoto', 
        'size', 
        'position', 
        'minsize', 
        'maxsize', 
        'resizable', 
        'transient', 
        'overrideredirect', 
        'windowtype', 
        'topmost', 
        'toolwindow', 
        'alpha',
        'relief',
        'border'
        )
    
    def __init__(self, master: Any = None, /, **kwargs) -> None:
        if master is None:
            master = app_manager.MAIN_WINDOW
        kwargs.setdefault('title', self.win_title if self.win_title else self.__class__.__name__)
        # Фильтруем атрибуты, чтобы лишние не были переданы в инициализатор окна
        super().__init__(master=master, **{x: y for x, y in kwargs.items() if x in self.__TK_KWARGS})   #type: ignore
        self.bind('<Escape>', lambda _: self.destroy())
        # Устанавливаем геометрию окна до основной отрисовки
        self.set_window_geometry()
        self.main(**kwargs)   
        self.focus_set()
        self.grab_set()
        
    def main(self, **kwargs) -> None:
        """
            Абстрактная ф-я для сборки других ф-й. 
            Запускается в момент инициализации объекта.
            В основном, служит для сборки ф-й отрисовки дочерних виджетов.
        """
        pass

    def set_window_geometry(self) -> None:
        """Установка размеров окна и центрирование его относительно центрального"""
        width, height = self.width, self.height

        place_x = ((self.master.winfo_width() - width) // 2) + self.master.winfo_x()
        place_y = ((self.master.winfo_height() - height) // 2) + self.master.winfo_y()
        
        self.geometry(f"{width}x{height}+{place_x}+{place_y}")
        self.resizable(False, False)
        self.update_idletasks()
