from ...source import *
from . import handlers


class ButtonsFrame(ttk.Frame):
    """Фрейм, который содержит в себе кнопки управления обработчиками."""

    def __init__(self, master: Any, /, **kwargs) -> None:
        super().__init__(master, **kwargs)
        for i in range(3):
            self.columnconfigure(i, weight=1)
        
        self.draw_left_column()
        self.draw_center_column()
        self.draw_right_column()
    
    def draw_left_column(self) -> None:
        """Отрисовка виджетов в левом столбике"""
        hl = HeaderLabel(self, text='Целевая обработка', anchor='n')

        btn1 = ttk.Button(
            self, 
            text='Разметка обложек', 
            # command=lambda: CoverMarkerWindow(self), 
            )
        btn2 = ttk.Button(
            self, 
            text='Раскодировка', 
            # command=lambda: PageDecoderWindow(master=self), 
            )
        btn3 = ttk.Button(
            self, 
            text='Направляющие', 
            # command=lambda:, 
            )
        btn4 = ttk.Button(
            self, 
            text='Холсты', 
            command=lambda: handlers.CanvasHandlerWindow(), 
            )
        for i, widget in enumerate((hl, btn1, btn2, btn3, btn4)):
            if i != 0:
                widget.configure(padding=2)
            widget.grid(row=i, column=0, sticky=ttkc.EW, padx=(0, 3), pady=(3, 0))

    def draw_center_column(self) -> None:
        """Отрисовка виджетов в центральном столбике"""
        hl = HeaderLabel(self, text='Файлы заказа', anchor='n')

        btn1 = ttk.Button(
            self, 
            text='Замена', 
            # command=lambda:, 
            )
        btn2 = ttk.Button(
            self, 
            text='Восстановление', 
            # command=lambda:, 
            )
        for i, widget in enumerate((hl, btn1, btn2)):
            if i != 0:
                widget.configure(padding=2)
            widget.grid(row=i, column=1, sticky=ttkc.EW, padx=(3, 3), pady=(3, 0))

    def draw_right_column(self) -> None:
        """Отрисовка виджетов в правом столбике"""
        hl = HeaderLabel(self, text='Дополнительно', anchor='n')

        btn1 = ttk.Button(
            self, 
            text='Роддом', 
            command=lambda: handlers.RoddomWindow(), 
            )

        for i, widget in enumerate((hl, btn1)):
            if i != 0:
                widget.configure(padding=2)
            widget.grid(row=i, column=2, sticky=ttkc.EW, padx=(3, 0), pady=(3, 0))
