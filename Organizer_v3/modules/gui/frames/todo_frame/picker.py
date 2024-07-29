from ...source import *
from datetime import datetime, timedelta
from typing import Callable, Literal


class UpButton(ttk.Button):
    """Кнопка вверх"""
    _text = '⋏'

    def __init__(self, master: Any, command: Callable[[], None], **kwargs) -> None:
        super().__init__(
            master, 
            style='link', 
            padding=1, 
            text=self._text, 
            command=command,
            **kwargs
        )


class DownButton(UpButton):
    """Кнопка вниз"""
    _text = '⋎'


class DatetimePicker(ttk.Frame):
    """Интерфейс для выбора дат и времени."""

    def __init__(self, master: Any, datetime: datetime, **kwargs):
        super().__init__(master, **kwargs)

        self.__datetime = datetime

        # Текстовые переменные для отображения информации о дате и времени
        self.__date_var = ttk.StringVar(self)
        self.__hour_var = ttk.StringVar(self)
        self.__minute_var = ttk.StringVar(self)
        self.__update_variables()

        # Отрисовка основных виджетов
        self.__draw_main_widgets()
    
    def get(self) -> datetime:
        """Возвращает объект дататайм - значение виджета."""
        return self.__datetime
    
    def __draw_main_widgets(self) -> None:
        """Отрисовка основных виджетов фрейма."""

        # Виджеты дат
        date_btn = ttk.Button(self, style='date', command=self.__date_picker_cmd)
        date_btn.grid(row=1, column=0, sticky='ns')

        date_up = UpButton(self, self.__dt_closure(timedelta(days=1)))
        date_up.grid(row=0, column=1, sticky=ttkc.EW)

        date_entry = ttk.Entry(
            self,
            state='readonly',
            width=10,
            textvariable=self.__date_var
        )
        date_entry.grid(row=1, column=1, sticky=ttkc.EW)

        date_down = DownButton(self, self.__dt_closure(timedelta(days=-1)))
        date_down.grid(row=2, column=1, sticky=ttkc.EW)

        # Виджеты времени
        hour_up = UpButton(self, self.__dt_closure(timedelta(hours=1)))
        hour_up.grid(row=0, column=2, sticky=ttkc.EW, padx=(5, 0))

        hour_entry = ttk.Entry(
            self, 
            width=2,
            state='readonly',
            textvariable=self.__hour_var
        )
        hour_entry.grid(row=1, column=2, padx=(5, 0))

        hour_down = DownButton(self, self.__dt_closure(timedelta(hours=-1)))
        hour_down.grid(row=2, column=2, sticky=ttkc.EW, padx=(5, 0))

        ttk.Label(self, text=':').grid(row=1, column=3)

        minute_up = UpButton(self, self.__dt_closure(timedelta(minutes=1)))
        minute_up.grid(row=0, column=4, sticky=ttkc.EW)

        minute_entry = ttk.Entry(
            self, 
            width=2,
            state='readonly',
            textvariable=self.__minute_var
        )
        minute_entry.grid(row=1, column=4)

        minute_down = DownButton(self, self.__dt_closure(timedelta(minutes=-1)))
        minute_down.grid(row=2, column=4, sticky=ttkc.EW)
    
    def __date_picker_cmd(self) -> None:
        """Выбор даты по нажатию на кнопку календаря."""
        date = Querybox().get_date(firstweekday=0)
        self.__datetime = datetime.combine(date, self.__datetime.time())
        self.__update_variables()

    def __dt_closure(self, delta: timedelta) -> Callable[[], None]:
        """
            Замыкание для работы с датами и временем.
            После совершения операции, обновляет текстовые переменные.
        """
        def inner() -> None:
            self.__datetime += delta
            self.__update_variables()

        return inner
    
    def __update_variables(self) -> None:
        """Обновление текстовых переменных."""
        self.__date_var.set(self.__datetime.strftime(r'%Y-%m-%d'))
        self.__hour_var.set(self.__datetime.strftime(r'%H'))
        self.__minute_var.set(self.__datetime.strftime(r'%M'))
