from ...source import *


class InitSampleWindow(ChildWindow):
    """Вспомогательное окно для заполнения переменных в текстовом шаблоне"""
    # Параметр height используется как множитель для растягивания окна
    width = 230
    height = 58
    _widgets = []

    def __init__(self, title: str, text: list[str, ...]) -> None:
        # Установка переменных
        self.win_title = title
        self._text = text

        # Получаем высоту окна в зависимости от количества полей в шаблоне
        self.height = 50 + len(text[1::2]) * self.height

        super().__init__()

        self._widgets[0].focus_set()
        self.bind('<Return>', self.create_sample)
    
    def main(self, **kwargs) -> None:
        self._widgets.clear()
        ttk.Label(master=self, text='Заполните поля:').pack()

        for var in self._text[1::2]:
            lbl = ttk.Label(master=self, text=var)
            lbl.pack(padx=(5, 0), anchor='nw')

            entry = ttk.Entry(master=self)
            entry.pack(padx=5, pady=(0, 5), fill=ttkc.X)

            self._widgets.append(entry)

        _ok = ttk.Button(
            self, 
            padding=2,
            width=8,
            text='Ок', 
            command=self.create_sample, 
            style='success'
        )
        _ok.pack(
            side=ttkc.LEFT, 
            padx=(5, 3), 
            pady=(0, 5), 
            fill=ttkc.X, 
            expand=1
        )

        _cancel = ttk.Button(
            self, 
            padding=2,
            width=8,
            text='Отмена', 
            command=self.destroy, 
            style='danger'
        )
        _cancel.pack(
            side=ttkc.RIGHT, 
            padx=(3, 5), 
            pady=(0, 5), 
            fill=ttkc.X, 
            expand=1
        )

    def create_sample(self, event: tkinter.Event | None = None):
        """Обновление списка self._text."""
        for i, v in enumerate(self._widgets):
            self._text[1 + i*2] = v.get()

        super().destroy()

    def destroy(self) -> None:
        """При вызове destroy очищаем список"""
        self._text.clear()
        super().destroy()
