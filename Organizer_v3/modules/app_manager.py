"""
    Модуль собирающий в себя критические объекты приложения.
    Для удобства, ссылки на объекты продублированы.
    Сделаны записи в верхнем регитсре, как константы.
    Присутствуют сокращения, в нижнем регистре.
"""


# Модуль дескрипторов
from .utilits import descriptors as DESCRIPTORS
desc = DESCRIPTORS


# Базы данных
from . import data_base
LIBRARY = lib = data_base.Library()
LOG = log = data_base.Log()
MAIL_SAMPLES = ms = data_base.MailSamples()


# Операционная система
from os import name as OS_NAME


# Объекты задач, очереди и обработки. Импортируются как типизация.
# Будут записаны в модуль во время инициализации основного окна
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gui.frames.todo_frame.main import TODOFrame
    from .gui.frames.file_frame.processing_frame import ProcessingFrame
    from .gui.frames.file_frame.queue_frame import QueueFrame

type _ProcessingFrame = ProcessingFrame
type _QueueFrame = QueueFrame
type _TODOFrame = TODOFrame

PROCESSING_FRAME: _ProcessingFrame = None       #type: ignore
pf = PROCESSING_FRAME
QUEUE: _QueueFrame = None                       #type: ignore
queue = QUEUE
TODOFRAME: _TODOFrame = None                    #type: ignore
tdf = TODOFRAME


# Менеджер потоков
from .utilits import thread_manager as THREAD_MANAGER


# Основное окно приложения
from .gui.main import MainWindow
MAIN_WINDOW = mw = MainWindow()


# Трекеры
from .trackers import *
ORDER_TRACKER = ot = OrdersTracker()    # Трекер заказов
TASK_TRACKER = tt = TaskTracker()       # Трекер задач
TASK_TRACKER.auto(1)                    # Работает всегда в автоматическом режиме


# Объект настроек инициализируем полседним.
# Он подтянет из файла настроек необходимые данные и 
# запустит приложение с нужной конфигурацией
SETTINGS = stg = data_base.Settings()



# Для теста
# pf.__exit__(None, None, None)
# pf.__enter__()