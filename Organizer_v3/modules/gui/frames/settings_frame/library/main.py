from ....source import *
from .assist import AssistWindow


class LibraryWindow(ChildWindow):
    """Окно управления библиотекой"""
    width = 550
    height = 400
    win_title = 'Библиотека'

    def __init__(self) -> None:
        super().__init__()
        self.container = ScrolledFrame(self, bootstyle='round')
        self.container.pack(fill=ttkc.BOTH, expand=1)
        self.draw_header_button()
        self.draw_main_widgets()
    
    def cmd_add_product(self, base: tuple) -> None:
        """Добавление нового продукта в библиотеку."""
        if base:
            name, *values = base
        else:
            prop = APP.lib.Properties
            name = prop.name()[0]
            values = (
                '!Новая категория!', prop.segment()[0], prop.short_name()[0], prop.format()[0],
                *(None for _ in range(len(APP.lib.Product._fields) - 5))
            )

        try: 
            APP.lib.add(APP.lib.Product(name, *values))   # type: ignore
            self.redraw()
        except Exception as e: 
            tkmb.showwarning('Ошибка', str(e), parent=self)
    
    def draw_header_button(self) -> None:
        """Отрисовка кнопки добавить"""
        btn = ttk.Button(
            self, 
            style='success', 
            padding=2,
            text='Добавить', 
            command=self.cmd_add_product
        )
        btn.place(anchor=ttkc.N, relx=0.5, y=3, width=80)

    def draw_main_widgets(self) -> None:
        """Отрисовка основных виджетов на основе полученной из библиотеки информации"""
        # Создаем словарь на основе полученных из библиотеки продуктов
        headers = APP.lib.get_headers()
        headers.sort()

        header = None
        headers_len = len(headers) - 1

        # Отрисовка виджетов
        for i, v in enumerate(headers):
            # Отрисовка заголовка
            if v[0] != header:
                header = v[0]
                h = HeaderLabel(self.container, v[0], padx=5)
                h.pack(anchor=ttkc.W, pady=(10, 3))
            
            # Отрисовка фрейма продукта
            end = i == headers_len or headers[i + 1][0] != header
            p = ProductFrame(self.container, end, v[1])
            p.pack(fill=ttkc.X, padx=(10, 10))

    def redraw(self) -> None:
        """Перерисовка виджетов в связи с обновлением библиотеки"""
        for widget in self.container.winfo_children():
            widget.destroy()
        self.draw_main_widgets()


class ProductFrame(ttk.Frame):
    """Фрейм для отображения продукта и взаимодействия с ним."""
    
    def __init__(self, master: Any, end: bool, name: str) -> None:
        super().__init__(master)

        # Направляющие
        ttk.Separator(self, orient='vertical').place(relheight=0.5 if end else 1)
        ttk.Separator(self, orient='horizontal').place(relwidth=0.5, rely=0.5)

        # Кнопка взаимодействия с продуктом
        btn = ttk.Button(
            self,
            command=lambda: AssistWindow(master.master.master, name),
            padding=1,
            style='ljf.Link.TButton',
            text=name
        )
        btn.pack(side=ttkc.LEFT, padx=(20, 0), fill=ttkc.X, expand=1)
