# Импорты для конструкции визуала
from ....source import *
from ....source import images
from ttkbootstrap.tooltip import ToolTip


# Импорты обработчиков
import modules.file_handlers.image_handlers as handlers


# Типизация
from typing import Callable


class HandlerWindow(ChildWindow):
    """Конструктор для окон обработчиков файлов"""
    # Геометрия окна
    width, height = 280, 194

    # Название окна и текстовая информация, используемая обработчиком
    win_title = 'Обработчик'
    handler_description = 'Описание того, что делает обработчик'
    handler_option_text = 'Опция обработчика'

    # Ссылка на объект - обработчик 
    file_handler = handlers.Handler

    def __init__(self):
        # Атрибуты обработчика
        self.onve: ONVEntry                         # Ссылка на энтри, в котором вводится номер заказа
        self.text_var: ttk.StringVar                # Текстовая переменная для отображения статуса обработчика
        self.handler_option: ttk.BooleanVar         # Переменная для фиксации дополнителной опции обработки
        self.target_combo: ttk.Combobox             # Ссылка на комбобокс целевых тиражей
        self.miss_combo: ttk.Combobox               # Ссылка на комбобокс пропускаемых тиражей
        self.order: APP.log.Order | None = None     # Ссылка на прокси объект

        super().__init__()
        self.onve.focus_set()

    def main(self, **kwargs):
        self.show_info_label()
        self.show_order_name_validate_widgets()
        self.show_handler_option_widget()
        self.show_target_edition_widgets()
        self.show_miss_edition_widgets()
        self.show_buttons()
        self.bind('<KeyPress>', self.__key_event)

    def __key_event(self, event: tkinter.Event) -> None:
        """
            Обработка нажатия кнопок. 
            Если Энтер - запуск обработчика.
            Остальные нажатия - перемещают фокус на энтри виджет
        """
        if event.keysym == 'KP_Enter' or event.keysym == 'Return':
            self.run_handler()
            return

        if self.onve != self.focus_get():
            self.onve.focus_set()
            self.onve.event_generate('<KeyPress>', keysym=event.keysym)
        
    def show_info_label(self) -> None:
        """Отрисовка лейбла с информацией - подсказкой"""
        info = ttk.Label(master=self, image=images.QUESTION)
        info.place(x=258, y=2)
        ToolTip(
            info, 
            bootstyle='primary-inverse', 
            text=self.handler_description, 
            width=1, 
            height=1
        )

    def show_order_name_validate_widgets(self) -> None:
        """Отрисовка виджета ввода имени заказа"""
        self.onve = onve = ONVEntry(self, _func=self.get_order)
        onve.pack(pady=(5, 0), padx=60, fill=ttkc.X)

        self.text_var = var = ttk.StringVar(master=self)
        ttk.Label(self, textvariable=var).pack(pady=(5, 0))
        
        ttk.Separator(self, orient='horizontal').pack(fill=ttkc.X, padx=5)

    def show_handler_option_widget(self) -> None:
        """Отрисовка виджета управления опциями обработчика"""
        self.handler_option = h_o = ttk.BooleanVar(master=self, value=True)

        chbtn = ttk.Checkbutton(self, text=self.handler_option_text, variable=h_o)
        chbtn.pack(anchor=ttkc.NW, padx=5, pady=5)

    def show_target_edition_widgets(self) -> None:
        """Отрисовка виджета тиражей, который будут обработаны"""
        self.target_combo = combo = ttk.Combobox(self, state='disabled')
        combo.pack(padx=5, fill=ttkc.X)
        combo.bind('<<ComboboxSelected>>', self.__combo_closure(combo, 'Целевые тиражи:'))

    def show_miss_edition_widgets(self) -> None:
        """Отрисовка виджета тиражей, которые будут пропущены обработчиком"""
        self.miss_combo = combo = ttk.Combobox(self, state='disabled')
        combo.pack(padx=5, pady=3, fill=ttkc.X)
        combo.bind('<<ComboboxSelected>>', self.__combo_closure(combo, 'Будут пропущенны:'))
    
    @staticmethod
    def __combo_closure(combo: ttk.Combobox, text: str) -> Callable[[Any], None]:
        """
            Замыкание, для предоставления функции, которое 
            возвращает значение комбобоксов к исходному - text
        """
        combo.set(text)

        def closure(_) -> None:
            combo.set(text)
            combo.select_clear()
        
        return closure

    def show_buttons(self) -> None:
        """Отрисовка кнопок"""
        start = ttk.Button(
            self, 
            width=15,
            padding=2,
            style='btn.success.TButton',
            text='Запуск', 
            command=self.run_handler
        )
        start.pack(
            side=ttkc.LEFT, 
            padx=(5, 3),
            pady=5,  
            fill=ttkc.X, 
            expand=1
        )

        cancel = ttk.Button(
            self, 
            width=15,
            style='warning',
            padding=2,
            text='Отмена', 
            command=self.destroy
        )
        cancel.pack(
            side=ttkc.RIGHT, 
            padx=(3, 5),
            pady=5,  
            fill=ttkc.X, 
            expand=1
        )

    def get_order(self, order_name: str) -> None:
        """Получение объекта заказа и выведение его элементов в виджете"""
        self.reset_to_default()
        order = APP.log.get(order_name)

        if order is None:
            self.text_var.set(f'Не могу найти заказ {order_name}')
            return

        self.update_combo(order)

    def update_combo(self, order: APP.log.Order) -> None:
        """
            Обновление значений виджета целевых тиражей. 
            Так же записывает прокси объект в общий словарь.
        """
        target, miss = [], []
        for edition in order.content:
            if edition.product and edition.product.type in self.file_handler.types:
                target.append(edition.name) 
            else:
                miss.append(edition.name)

        if target:
            self.text_var.set(f'Обработка {order.name}')
            self.target_combo.config(values=target, state='readonly')
            self.order = order
        else:
            self.text_var.set(f'В заказе {order.name} нет целевых тиражей')

        if miss:
            self.miss_combo.config(values=miss, state='readonly')

    def run_handler(self):
        """Функция запуска обработчика"""
        if not self.order:
            tkmb.showwarning(
                parent=self, 
                title=self.win_title, 
                message='Не указан заказ или в заказе нет целевых тиражей.'
            )
            return

        # Постановка на обработку
        APP.tm.create_task(
            self.file_handler, #type: ignore
            self.order, 
            self.handler_option.get()
        ) 
        # Сообщение о успехе
        tkmb.showinfo(
            parent=self, 
            title=self.win_title, 
            message=f'Заказ {self.order.name} поставлен в очередь обработки'
        )
        self.reset_to_default()

    def reset_to_default(self):
        """Возвращение к стартовым значениям"""
        self.order = None
        self.text_var.set('')
        self.target_combo.config(values=tuple(), state='disabled')
        self.miss_combo.config(values=tuple(), state='disabled')
