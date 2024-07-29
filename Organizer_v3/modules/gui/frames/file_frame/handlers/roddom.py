from modules.gui.source import *
from modules.file_handlers.roddom import RoddomHandler


class RoddomWindow(ChildWindow):
    """Окно управления заказами роддома"""
    width = 315
    height = 230
    win_title='Роддом'
    
    def main(self, **kwargs) -> None:
        # Переменные, необходимые для работы
        self.order_obj = None

        self.show_directory_widget()

        self.text_field: ttk.Text
        self.show_info_widget()

        self.txt_sum = ttk.BooleanVar(master=self, value=True)
        self.show_buttons()

    def show_directory_widget(self) -> None:
        """Отрисовка виджета отображения папки роддома и кнопки ее смены"""
        def update_dir() -> None:
            """Функция смены папки роддома"""
            path = tkfd.askdirectory()
            if path:
                APP.stg.roddom_dir = path
                upd.var.set(path)
            
        HeaderLabel(self, text='Папка с заказами Роддом\'а').pack(fill=ttkc.X, padx=5, pady=(5, 2))

        upd = SettingLine(self, update_dir)
        upd.var.set(APP.stg.roddom_dir)
        upd.pack(fill=ttkc.X, padx=10)

    def show_info_widget(self) -> None:
        """Отрисовка виджета информации о заказе"""
        default_text = "Для подсчета количества отпечатков в заказе, нажмите на кнопку \'Посчитать заказ\' и выберете нужную папку."

        self.text_field = ttk.Text(
            self, 
            height=4,       # минимальная высота, которая нужна для отображения полной инфомрации
            wrap='word',  
            font="TkTextFont 11 normal roman",
            state='disabled'
            )
        self.text_field.pack(padx=5, pady=(10, 5), fill=ttkc.BOTH, expand=1)
        self._update_text_field(default_text)
    
    def _update_text_field(self, text: str) -> None:
        """Обновляет текстовое поле."""
        self.text_field.configure(state='normal')
        self.text_field.delete('1.0', ttkc.END)
        self.text_field.insert('1.0', text)
        self.text_field.configure(state='disabled')

    def show_buttons(self) -> None:
        """Отрисовка виджетов кнопок"""
        chbtn = ttk.Checkbutton(
            self, 
            text='Сохранять результаты в sum.txt', 
            variable=self.txt_sum,
            style='success-round-toggle'
            )
        chbtn.pack(anchor=ttkc.W, padx=5, pady=(0, 5))

        btn1 = ttk.Button(
            self, 
            width=20,
            padding=2,
            text='Посчитать заказ', 
            command=self.calc_order
            )
        btn1.pack(padx=(5, 3), pady=(0, 5), fill=ttkc.X, side=ttkc.LEFT)

        btn2 = ttk.Button(
            self, 
            width=20,
            padding=2,
            text='Отправить в печать', 
            command=self.to_print
            )
        btn2.pack(padx=(3, 5), pady=(0, 5), fill=ttkc.X, side=ttkc.RIGHT)

    def calc_order(self):
        """Инициализация подсчета информации в заказе"""
        path = tkfd.askdirectory(parent=self, initialdir=APP.stg.roddom_dir)
        if not path:
            return
        self.order_obj = RoddomHandler(path, self.txt_sum.get())
        day = '-'.join(self.order_obj.order.split('-')[::-1])
        info = '\n'.join(f'{" "*5}{k}: {v}' for k, v in self.order_obj.get_calc_info().items())
        self._update_text_field(f'{day}\n{info}')

    def to_print(self):
        """Отправка заказа в печать"""
        # Проверка на существование заказа
        if self.order_obj is None:
            tkmb.showwarning(parent=self, title='Отправка в печать', message='Заказ не выбран')
            return

        # Получение пути
        path = tkfd.askdirectory(parent=self, initialdir=APP.stg.t_disc)
        if not path: return

        # Вставка информации в буфер обмена
        self.clipboard_clear()
        self.clipboard_append(f'{path}/{self.order_obj.order}\n\n{self.order_obj.order} -- Роддом')

        # Отправка в печать / копирование на диск
        self.order_obj.to_print(path)
        tkmb.showinfo(
            parent=self, 
            title='Отправка в печать', 
            message=f'Заказ {self.order_obj.order} отправлен в печать'
            )
