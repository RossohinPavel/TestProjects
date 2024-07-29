"""
    Модуль для запуска параллельных потоков программы.
    Предоставляет 2 декораторя для ф-й:
    parallel - Для запуска функции в прараллельном потоке без ограничений.
    in_queue -  Для запуска функции в прараллельном потоке ограниченное очередью.
    Прядок очереди определяется порядком вызовов. Используется, в основном,
    для обработки файлов.
"""
from threading import Thread, Lock
import modules.app_manager as APP
from typing import Callable, ParamSpec


# При помощи объекта Lock реализуем очередь
_LOCK = Lock()


# Хинтинг для типизации аргументов
P = ParamSpec('P')


def parallel(func: Callable[P, None]):
    """Декоратор для запуска ф-ии в параллельном потоке."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        t = Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        t.start()
    
    return wrapper


def __queue_closure(func: Callable[P, None]):
    """Замыкание, для взаимодействия с очередью."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        with APP.queue, _LOCK, APP.pf:
            return func(*args, **kwargs)

    return wrapper


def in_queue(func: Callable[P, None]):
    """
        Декоратор для постановки ф-ии в очередь выполнения и ее запуск.
        Помимо очереди, активирует контекстые менеджеры очереди и обработки файлов.
    """
    func = __queue_closure(func)    #type: ignore

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        parallel(func)(*args, **kwargs)

    return wrapper
