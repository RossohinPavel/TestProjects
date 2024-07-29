__all__ = ('print_func_call', 'print_method_call', 'func_time_test')
import time


def print_func_call(func):
    def wrapper(*args, **kwargs):
        print(f'Вызов функции {func.__name__}')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def print_method_call(cls):
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)):
            setattr(cls, attr, print_func_call(getattr(cls, attr)))
    return cls


def func_time_test(cycles=100):
    """тестирование ф-ии на время выполнения"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            for _ in range(cycles):
                func(*args, **kwargs)
            res = func(*args, **kwargs)
            print(f'Время {cycles} циклов функции {wrapper.__name__} -', time.time() - start)
            return res
        return wrapper
    return decorator
