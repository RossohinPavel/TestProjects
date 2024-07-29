from abc import ABC, abstractmethod
from threading import Thread
from time import sleep, time


class TrackerThread(Thread):
    """Параллельный поток, который запускает выполнение трекера в автоматическом режиме"""
    
    def __init__(self, tracker) -> None:
        self.tracker: Tracker = tracker
        self.is_repeating = True
        super().__init__(daemon=True)

    def run(self) -> None:
        """Зацикливает поток, запуская автоматический режим трекера"""
        while self.is_repeating:
            start = time()
            self.tracker.auto_init()
            sleep(start - time() + self.tracker.delay)


class Tracker(ABC):
    """
        Абстрактный класс реализующий общую логику работы трекера.
        Публичные ф-ии используются для запуска трекера 
        в автоматическом (auto_init) или ручном режимах (manual_init).
    """

    __slots__ = ('delay', '_thread')

    def __init__(self) -> None:
        # Стандартный цикл работы трекера в 150 секунд - 2,5 минуты
        self.delay = 150

        # Поток, в котором запускается автоматическая функция трекера
        self._thread = TrackerThread(self)
    
    def auto(self, value: int) -> None:
        """
            Включает или выключает автоматический режим трекера 
            в зависимости от переданного значения
        """
        match value:
            case 0:
                # Выключаем повторение на текущем потоке и перезаряжаем его))
                self._thread.is_repeating = False
                self._thread = TrackerThread(self)
            case _:
                self._thread.start()

    @abstractmethod
    def auto_init(self) -> None:
        """Реализует логику работы трекера в автоматическом режиме."""

    @abstractmethod
    def manual_init(self) -> None:
        """Реализует логику работы трекера в ручном режиме."""
