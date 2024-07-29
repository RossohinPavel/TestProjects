import modules.app_manager as APP


class OrderProxy:
    """
        Основа для наследования. Получает заказ из лога заказов.
        Реализует базовые методы работы с прокси объектом.
    """

    __slots__ = 'order', 

    def __init__(self, order_name: str) -> None:
        self.order: APP.log.Order = APP.log.get(order_name) #type: ignore
    
    def __bool__(self):
        return bool(self.order)
