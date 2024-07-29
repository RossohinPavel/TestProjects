import timeit
import sys


def time_and_size(func):
    def wrapper(*args, **kwargs):
        st = timeit.default_timer()
        obj = func(*args, **kwargs)
        et = timeit.default_timer()
        it = et - st
        size1 = obj.__sizeof__()
        size2 = sys.getsizeof(obj)
        print(f"{func.__name__}: {it} / {size1} - {size2}")
        return obj
    return wrapper
