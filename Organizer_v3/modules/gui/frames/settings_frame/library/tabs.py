from ....source import *
from ....source import images


class LineFrame(ttk.Frame):
    """Конструктор для отрисовки линии настроек"""

    def __init__(self, master: Any, attr: str, assist_window: Any, **kwargs):
        super().__init__(master)
        self._product: dict = assist_window._product                # Ссылка на объект Product
        self._vars: dict = assist_window._vars                      # Ссылка на словарь, со всеми атрибутами

        self._attr = attr                                           # Название атрибута объекта _product
        self._values = getattr(APP.lib.Properties, attr)()          # Кортеж элементов для виджета
        self._str_var = ttk.StringVar(self)                         # Текстовая переменная виджета

        # Переменная для хранения виджетов
        self._widgets = ()

        # Отрисовка основных атрибутов
        self.draw_text(kwargs)                   
        self.draw_main_widget(kwargs)      

        # По умолчанию, виджеты находятся в деактивированном состоянии.
        # Дополнительно, эта команда создаст в словаре self._vars необходимый атрибут
        self.deactivate()

    def draw_text(self, kwargs: dict) -> None:
        """Отрисовка текста фрема"""
        text = kwargs.get('text', '')
        if text: 
            lbl = ttk.Label(self, text=text)
            self._widgets = (lbl, )
            lbl.pack(anchor=ttkc.NW)
    
    def draw_main_widget(self, kwargs: dict) -> None:
        """Отрисовка основного виджета"""
        match kwargs['widget']:
            case 'combo': self.__draw_combobox_widget()
            case 'radio': self.__draw_radio_widgets()
            case 'entry' | _: self.__draw_entry_widget()
    
    def __draw_combobox_widget(self):
        """Конструктор для отрисовки Комбобокс виджета"""
        # Рисуем Комбобокс
        combo = ttk.Combobox(
            master=self, 
            state='readonly', 
            values=sorted(self._values),
            textvariable=self._str_var,
            cursor='hand2'
        )
        combo.pack(fill=ttkc.X)
        self._widgets += (combo, )

    def __draw_entry_widget(self):
        """Конструктор отрисовки Entry виджета"""
        entry = ttk.Entry(self, textvariable=self._str_var)
        entry.pack(fill=ttkc.X)
        self._widgets += (entry, )

    def __draw_radio_widgets(self):
        """Конструктор для отрисовки Радио-баттон-виджетов"""
        # Отрисовки линий виджетов радиобаттонов
        line = None
        # Рисуем Radiobutton'ы
        for i, name in enumerate(self._values):
            if i % 3 == 0:
                line = ttk.Frame(self)
                line.pack(anchor=ttkc.NW, expand=1)

            rbtn = ttk.Radiobutton(master=line, text=name, value=name, variable=self._str_var)
            self._widgets += (rbtn, )
            rbtn.pack(padx=(5, 10), pady=5, anchor=ttkc.NW, side=ttkc.LEFT)
    
    def activate(self) -> None:
        """
            Активирует связанные виджеты. 
            Помещает текстовую переменныю в словарь self._vars.
            Мняет режим виджетов на нормальный.
        """
        self._vars[self._attr] = self._str_var
        attr_value = self._product[self._attr]
        if attr_value is None:
            attr_value = self._values[0]
        self._str_var.set(attr_value)
        for widget in self._widgets:
            if isinstance(widget, ttk.Label):
                widget.configure(bootstyle='default')       #type: ignore

            state = 'normal'
            if isinstance(widget, ttk.Combobox):
                state = 'readonly'
        
            widget.configure(state=state)
    
    def deactivate(self) -> None:
        """
            Деактивирует связанные виджеты. 
            Помещает None в словарь self._vars.
            Меняет положение виджетов на выключенный.
        """
        self._vars[self._attr] = None
        self._str_var.set('')
        for widget in self._widgets:
            if isinstance(widget, ttk.Label):
                widget.configure(bootstyle='secondary')     #type: ignore
            widget.configure(state='disabled')


class SwitchedLine(ttk.Frame):
    """Конструктор переключаемой линии"""

    def __init__(self, master: Any, name: str):
        super().__init__(master)
        self._int_var = ttk.IntVar(self)
        self._widgets: tuple[LineFrame, ...] = ()    #type: ignore
        self._chbtn = ttk.Checkbutton(
            self, 
            style="success-round-toggle",
            text=name,
            offvalue=0,
            onvalue=1,
            variable=self._int_var,
            command=self.command
        )
        self._chbtn.pack(anchor=ttkc.NW, fill=ttkc.X, expand=1)
    
    def command(self) -> None:
        """Переключает состояние виджетов"""
        match self._int_var.get():
            case 0: command = 'deactivate'
            case 1 | _: command = 'activate'

        for widget in self._widgets:
            eval(f'widget.{command}()')
    
    def add_widgets(self, *widgets: LineFrame) -> None:
        """
            Добавляет виджеты в self._widgets. Дополнительно проверяет, 
            содержат ли соответствующие переменные значения.
        """
        self._widgets = widgets 
        is_active = False
        for widget in widgets:
            if widget._product[widget._attr] is not None:
                is_active = True
        if is_active:
            self._chbtn.invoke()


class Tab(ttk.Frame):
    """
        Класс - вкладка для отрисовки виджетов в библиотеке.
        Включает общие для всех закладок методы.
    """

    def __init__(self, master: Any, assist_window: Any):
        super().__init__(master, padding=5)
        for i in range(2):
            self.columnconfigure(i, weight=1)


class CommonTab(Tab):
    """Отрисовка вкладки с обязательными атрибутами продукта."""

    def __init__(self, master: Any, assist_window: Any):
        super().__init__(master, assist_window)

        # Полное имя продукта
        name = LineFrame(self, 'name', assist_window, text='Название продукта', widget='entry')
        name.grid(row=0, column=0, columnspan=2, sticky=ttkc.EW, pady=(0, 5))
        name.activate()

        # Тип продукта
        type = LineFrame(self, 'type', assist_window, text='Тип продукта', widget='combo')
        type.grid(row=2, column=0, sticky=ttkc.EW, pady=(0, 5), padx=(0, 3))
        type.activate()

        # Сегмент
        segment = LineFrame(self, 'segment', assist_window, text='Сегмент', widget='radio')
        segment.grid(row=2, column=1, sticky=ttkc.EW, pady=(0, 5), padx=(3, 0))
        segment.activate()

        # Короткое имя
        short_name = LineFrame(self, 'short_name', assist_window, text='Короткое имя', widget='combo')
        short_name.grid(row=4, column=0, sticky=ttkc.EW, pady=(0, 5), padx=(0, 3))
        short_name.activate()

        # Формат продукта
        format = LineFrame(self, 'format', assist_window, text='Формат продукта', widget='combo')
        format.grid(row=4, column=1, sticky=ttkc.EW, pady=(0, 5), padx=(3, 0))
        format.activate()

        self.rowconfigure(6, weight=1)
        container = ttk.Frame(self)
        container.grid(row=6, column=0, columnspan=2, sticky=ttkc.NSEW)

        copy = ttk.Button(
            container,
            command=assist_window.cmd_copy_product,
            image=images.COPY,
            padding=1,
            style='success'
        )
        copy.pack(side=ttkc.LEFT, anchor=ttkc.SE, expand=1, padx=5)

        delete = ttk.Button(
            container,
            command=assist_window.cmd_delete_product,
            image=images.DELETE,
            padding=1,
            style='danger'
        )
        delete.pack(side=ttkc.LEFT, anchor=ttkc.SE)


class CoverTab(Tab):
    """Отрисовка вкладки для атрибутов обложки"""
    def __init__(self, master: Any, assist_window: Any):
        super().__init__(master, assist_window)

        # Блок редактирования значений книжной обложки
        cover = SwitchedLine(self, 'Книжная обложка')
        cover_type = LineFrame(self, 'cover_type', assist_window, widget='radio')
        carton_length = LineFrame(self, 'carton_length', assist_window, widget='entry', text='ДЛИННА картонки')
        carton_height = LineFrame(self, 'carton_height', assist_window, widget='entry', text='ВЫСОТА картонки')
        cover_flap = LineFrame(self, 'cover_flap', assist_window, widget='entry', text='Размер клапана')
        cover_joint = LineFrame(self, 'cover_joint', assist_window, widget='entry', text='Размер шарнира')

        cover.add_widgets(cover_type, carton_length, carton_height, cover_flap, cover_joint)

        cover.grid(row=0, column=0, columnspan=2, sticky=ttkc.W)
        cover_type.grid(row=1, column=0, columnspan=2, sticky=ttkc.W, padx=(23, 0), pady=(0, 5))
        carton_length.grid(row=2, column=0, sticky=ttkc.EW, padx=(0, 3), pady=(0, 5))
        carton_height.grid(row=2, column=1, sticky=ttkc.EW, padx=(3, 0), pady=(0, 5))
        cover_flap.grid(row=3, column=0, sticky=ttkc.EW, padx=(0, 3), pady=(0, 5))
        cover_joint.grid(row=3, column=1, sticky=ttkc.EW, padx=(3, 0), pady=(0, 5))

        # Печатный материал обложки
        print_mat = SwitchedLine(self, 'Материал обложки')
        print_mat_combo = LineFrame(self, 'cover_print_mat', assist_window, widget='combo')

        print_mat.add_widgets(print_mat_combo)

        print_mat.grid(row=4, column=0, sticky=ttkc.W, pady=(10, 0))
        print_mat_combo.grid(row=5, column=0, sticky=ttkc.EW, padx=(0, 3), pady=5)

        # Ламинация обложки
        cover_lam = SwitchedLine(self, 'Ламинация обложки')
        cover_lam_radio = LineFrame(self, 'cover_lam', assist_window, widget='radio')

        cover_lam.add_widgets(cover_lam_radio)

        cover_lam.grid(row=4, column=1, sticky=ttkc.W, pady=(10, 0), padx=(3, 15))
        cover_lam_radio.grid(row=5, column=1, sticky=ttkc.EW, padx=(3, 0), pady=5)


class BlockTab(Tab):
    """Отрисовка вкладки для атрибутов внутреннего блока"""
    def __init__(self, master: Any, assist_window: Any):
        super().__init__(master, assist_window)

        # Опция сборки книжного блока
        page_option = SwitchedLine(self, 'Опция сборки книжного блока')
        page_option_radio = LineFrame(self, 'page_option', assist_window, widget='radio')

        page_option.add_widgets(page_option_radio)

        page_option.grid(row=0, column=0, sticky=ttkc.EW, columnspan=2, pady=(5, 0))
        page_option_radio.grid(row=1, column=0, sticky=ttkc.EW, padx=(25, 0), pady=(0, 5), columnspan=2)

        # Печатный матерал блока
        print_mat = SwitchedLine(self, 'Материал блока')
        print_mat_combo = LineFrame(self, 'page_print_mat', assist_window, widget='combo')

        print_mat.add_widgets(print_mat_combo)

        print_mat.grid(row=2, column=0, sticky=ttkc.EW, pady=(10, 0))
        print_mat_combo.grid(row=3, column=0, sticky=ttkc.EW, pady=5, padx=(0, 3))

        # Печатный матерал блока
        page_lam = SwitchedLine(self, 'Ламинация блока')
        page_lam_radio = LineFrame(self, 'page_lam', assist_window, widget='radio')

        page_lam.add_widgets(page_lam_radio)

        page_lam.grid(row=2, column=1, sticky=ttkc.EW, padx=(3, 30), pady=(10, 0))
        page_lam_radio.grid(row=3, column=1, sticky=ttkc.EW, padx=(3, 0), pady=5)

        # Раскодировки
        dc = SwitchedLine(self, 'Раскодировка')
        dc_type = LineFrame(self, 'dc_type', assist_window, widget='combo', text='Тип раскодировки')
        dc_top_indent = LineFrame(self, 'dc_top_indent', assist_window, widget='entry', text='Отступ СВЕРХУ')
        dc_left_indent = LineFrame(self, 'dc_left_indent', assist_window, widget='entry', text='Отступ СЛЕВА')
        dc_overlap = LineFrame(self, 'dc_overlap', assist_window, widget='entry', text='Размер нахлеста')

        dc.add_widgets(dc_type, dc_top_indent, dc_left_indent, dc_overlap)

        dc.grid(row=4, column=0, columnspan=2, sticky=ttkc.W, pady=(10, 5))
        dc_type.grid(row=5, column=0, sticky=ttkc.EW, padx=(0, 3), pady=(0, 5))
        dc_top_indent.grid(row=5, column=1, sticky=ttkc.EW, padx=(3, 0), pady=(0, 5))
        dc_left_indent.grid(row=6, column=0, sticky=ttkc.EW, padx=(0, 3), pady=(0, 5))
        dc_overlap.grid(row=6, column=1, sticky=ttkc.EW, padx=(3, 0), pady=(0, 5))
