from ...source import *


class ProcessingFrame(ttk.Frame):
    """
        Фрейм отображающий статус обработки различных задач. 
        Используется как контекстный менеджер
    """
    
    def __init__(self, master: Any):
        super().__init__(master, height=80)

        # Лейбл для отображения названия модуля
        self.header = ModuleLabel(self)

        # Интерфейс операций
        self.operation = OperationLabel(self)

        # Файловый интерфейс
        self.filebar = FileBar(self)

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        APP.mw.file.show_badge()
        self.header.place(x=0, y=0)
        self.operation.place(x=0, y=20)
        self.filebar.place(x=0, y=40)

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        if exc_value:
            tkmb.showerror('Ошибка', message=f'{repr(exc_type)}\n{exc_value.args}')

        APP.mw.file.hide_badge()
        for widget in (self.header, self.operation, self.filebar):
            widget.reset()
            widget.place_forget()

        return True


class ModuleLabel(ttk.Label):
    """Интерфейс для текста заголовка"""

    def step(self, value: str):
        """Установка текста лейбла"""
        self.configure(text=value)
    
    def reset(self):
        """Сбрасывает значения виджетов до начальных"""
        self.configure(text='__DEBUG__ from ModuleLabel')


class OperationLabel(ttk.Label):
    """Интерфейс для упрощения обработки операций и их названий"""

    def __init__(self, master: Any) -> None:
        super().__init__(master)
        self.__value = 0
        self.maximum = 1

    def step(self, value: str) -> None:
        """Установка значения в текстовую переменную"""
        self.__value += 1
        prefix = f'{self.__value} / {self.maximum} -- ' if self.maximum > 1 else ''
        self.configure(text=f'{prefix}{value}')
    
    def reset(self) -> None:
        """Сбрасывает значения виджетов до начальных"""
        self.__value = 0
        self.maximum = 1
        self.configure(text='__DEBUG__ from OperationLabel')


class FileBar:
    """Интерфейс для управления виджетами файлов"""

    def __init__(self, master: Any) -> None:
        # Лейбл отображения имени файла
        self.__file_lbl = ttk.Label(master)

        # Прогрессбар
        self.__pb = ttk.Progressbar(master, style='success-striped')

        # Переменные для прогрессбара и лейблов
        self.__value = 1        # int Переменная для подсчета количества обработанных файлов
        self.__maximum = 100    # int Переменная для отображения общего количества обрабатываемых фалов

        self.__delta = 1.0      # float Переменная, отображающая значение, на которое увеличивается ProgressBar
        self.__percent = 0.0    # float переменная, для подсчета пройденных процентов. Для того, чтобы не обращаться в прогрессбар
        
    def place(self, x: int = 0, y: int = 0) -> None:
        """Метод, запускающий одноименный метод в лейбле и прогрессбаре"""
        self.__file_lbl.place(x=x, y=y)
        self.__pb.place(x=x, y=y+25, relwidth=1)
    
    def place_forget(self) -> None:
        """Метод, запускающий одноименный метод в лейбле и прогрессбаре"""
        self.__file_lbl.place_forget()
        self.__pb.place_forget()
    
    def reset(self) -> None:
        """Сбрасывает значения виджетов до начальных"""
        self.__file_lbl.configure(text='__DEBUG__ from FileBar')
        self.__pb['value'] = self.__percent = 0.0
        self.__value = 1
        self.__delta = 1.0
        self.__maximum = 100

    def maximum(self, value: int, percentage: int = 100) -> None:
        """
            Устанавливает предельное значение
            value: общее количество шагов (файлов, объектов и т.д)
            percentage: Сколько в процентном соотношении от 100, займет прогрессия 
        """
        self.__maximum = value
        self.__delta = percentage / value
        self.__value = 0
    
    def step(self, value: str) -> None:
        """Начало шага. Устанавливает значение в текстовую переменную"""
        self.__value += 1
        if self.__maximum > 1:
            percent = str(round(self.__percent, 1)) + '% '
            prefix = f'({self.__value} / {self.__maximum}) -- '
        else:
            percent = prefix = ''
        self.__file_lbl.configure(text=f'{percent}{prefix}{value}')
        
    def step_end(self) -> None:
        """Конец шага. Продвигает прогрессбар"""
        self.__percent += self.__delta
        self.__pb['value'] += self.__delta
