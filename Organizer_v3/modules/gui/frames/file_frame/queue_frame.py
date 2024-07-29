from ...source import *


class QueueFrame(HeaderLabel):
    """
        Фрейм для отображения статуса очереди задач.
        Работает как контекстный менеджер.
    """

    def __init__(self, master: Any):
        self.value = 0
        super().__init__(master)
        self.update_status()
    
    def update_status(self) -> None:
        """Обновляет статус очереди задач на лейбле"""
        self.lbl.configure(text=f'Задач в очереди: {self.value}')
    
    def __enter__(self) -> None:
        """При входе в менеджер - увеличиваем очередь на 1 и обновляем лейбл"""
        self.value += 1
        self.update_status()
    
    def __exit__(self, *_) -> None:
        """При выходе - уменьшаем очередь и обновляем лейбл"""
        self.value -= 1
        self.update_status()
