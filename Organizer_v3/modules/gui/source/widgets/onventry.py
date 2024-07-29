from ..main import ttk, Any
from re import match as re_match
from typing import Callable


class ONVEntry(ttk.Entry):
    """Класс для отрисовки фреймов проверки заказа и осуществления логики первичной валидации номера"""
    def __init__(self, master: Any, _func: Callable[[str], None], **kwargs):
        self._func = _func
        super().__init__(master, validate='key', **kwargs)
        self.__insert_def_val()
        self.bind('<KeyPress>', self.__enter_event)
        self.config(validatecommand=(self.register(self.__validate), "%P"))

    def __enter_event(self, event):
        """Событие для очитски виджета от от текста, который там находится по умолчанию"""
        if self.get().startswith('#') and event.char.isdigit():
            self.delete(0, 'end')

    def __validate(self, value: str) -> bool:
        """Валидация введеных значений, вызов функции при полной валидации и очистка _entry"""
        res = re_match(r'\d{0,6}$', value) is not None
        if res and len(value) == 6:
            self._func(value)
            self.__insert_def_val()
        return res

    def __insert_def_val(self) -> None:
        """Очитска _entry и вставка значения по умолчанию"""
        self.delete(0, 'end')
        self.insert(0, '#Введите номер заказа')
        self.icursor(0)
