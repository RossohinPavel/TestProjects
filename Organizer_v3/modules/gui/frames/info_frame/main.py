from ...source import *
from .orders_stat_window import OrdersStatWindow
from .info_proxy import OrderInfoProxy


class InfoFrame(ttk.Frame):
    """Фрейм с отображением различной информации."""

    def __init__(self, master: Any) -> None:
        super().__init__(master, padding=5)
        # Верхнаяя чать - Поле ввода
        ONVEntry(self, self.cmd_insert_order_info).pack(fill=ttkc.X, pady=(0, 5))

        container = ttk.Frame(self)
        container.pack(fill=ttkc.BOTH, expand=1)

        # Текстовое поле
        self.field = ttk.Text(container, wrap='word', width=1, height=1)
        self.field.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1)

        scroll = ttk.Scrollbar(container, command=self.field.yview)
        scroll.pack(side=ttkc.RIGHT, fill=ttkc.Y)
        self.field.configure(yscrollcommand=scroll.set)

        self.draw_additional_line()
    
    def cmd_insert_order_info(self, order_name: str) -> None:
        """После валидации введенного номера, обновляет лейбл"""
        # Очитка текстового поля
        self.field.delete('1.0', ttkc.END)
        
        # Пытаемся получить прокси объект
        proxy = OrderInfoProxy(order_name)

        # Если заказа нет
        if not proxy:
            self.field.insert('1.0', f'Не могу найти заказ {order_name}')
            return

        # Формируем общую информацию
        self.field.insert('1.0', f'{proxy.order.name} - {proxy.order.customer_name}\n')
        self.field.insert(ttkc.END, f'Доставка: {proxy.order.customer_address}\n')
        self.field.insert(ttkc.END, f'Сумма: {proxy.order.price}\n')

        if proxy.order.content:
            self.field.insert(ttkc.END, '\n---- Тиражи ----')

        # Если в заказе есть тиражи
        for content in proxy.order.content:
            for i, info in enumerate(proxy.get_edition_info(content)):
                self.field.insert(ttkc.END, f'{'\n- ' if i == 0 else '      '}{info}\n')

        if proxy.order.photo:
            self.field.insert(ttkc.END, '\n---- Фотопечать ----\n')
        
        for photo in proxy.order.photo:
            self.field.insert(ttkc.END, f'      {photo.name}: {photo.value}шт\n')

    
    def draw_additional_line(self) -> None:
        """Отрисовка кнопок информации"""
        container = ttk.Frame(self, padding=(0, 5, 0, 0))
        container.pack(fill=ttkc.X)

        b1 = ttk.Button(
            container, 
            padding=2,
            width=16,
            text='Заказы', 
            command=lambda: OrdersStatWindow()
        )
        b1.pack(expand=1, anchor=ttkc.E, side=ttkc.LEFT, padx=5)
        b2 = ttk.Button(
            container, 
            padding=2,
            width=16,
            text='Клиенты', 
            # command=lambda: print(b1.winfo_geometry())
        )
        b2.pack(side=ttkc.LEFT)
