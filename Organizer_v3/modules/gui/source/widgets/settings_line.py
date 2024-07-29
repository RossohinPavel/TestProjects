from ..main import ttk, ttkc, Any
from .. import images
from typing import Callable, Type


class SettingLine(ttk.Frame):
    """Конструктор для отображения кнопки с иконкой шестеренки и лейбла настроек."""

    def __init__(
        self,
        master: Any, 
        command: Type[Callable[[], None]],
        _prefix: str = '',
        _postfix: str = ''
        ):
        super().__init__(master)

        if command is None:
            command = lambda: print(btn.winfo_geometry())

        # Кнопка вызова настроек
        btn = ttk.Button(
            self, 
            padding=1,
            image=images.GEAR,
            command=command,
        )
        btn.pack(anchor=ttkc.W, side=ttkc.LEFT)

        # Лейбл для отображения текста приставки, поясняющей суть настройки
        if _prefix:
            ttk.Label(self, text=_prefix).pack(anchor=ttkc.W, side=ttkc.LEFT)
        
        # Лейбл для отображения информации, полученной в результате вызова функции настройки
        self.var = ttk.StringVar(self)
        ttk.Label(self, textvariable=self.var).pack(anchor=ttkc.W, side=ttkc.LEFT)

        # Лейбл для отображения текста суффикса, поясняющей суть настройки
        if _postfix:
            ttk.Label(self, text=_postfix).pack(anchor=ttkc.W, side=ttkc.LEFT)
