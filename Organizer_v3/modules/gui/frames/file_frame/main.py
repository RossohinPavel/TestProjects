from ...source import *
from .queue_frame import QueueFrame
from .processing_frame import ProcessingFrame
from .tracker_frame import TrackerFrame
from .buttons_frame import ButtonsFrame


class FileFrame(ttk.Frame):
    """
        Фрейм отображающий статус обработки файлов. 
        Содержит кнопки запуска обработки.
    """

    def __init__(self, master: Any) -> None:
        super().__init__(master, padding=5)

        # Отображение очереди задач
        APP.queue = APP.QUEUE = queue = QueueFrame(self)
        queue.pack(fill=ttkc.X)

        # Отображение фрейма статуса обработки
        APP.pf = APP.PROCESSING_FRAME = pf = ProcessingFrame(self)
        pf.pack(fill=ttkc.X, padx=5, pady=(2, 20))

        # Фрейм кнопок 
        ButtonsFrame(self).pack(fill=ttkc.X, pady=(0, 20))

        # Фрейм трекера заказов
        TrackerFrame(self).pack(fill=ttkc.X)
