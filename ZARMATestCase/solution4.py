"""
Решение 4 задачи: 
Дан следующий скрипт на Python для обработки списка чисел. Оптимизируйте его для повышения производительности.

numbers = [i for i in range(1, 1000001)]
squares = []
for number in numbers:
    squares.append(number ** 2)
"""
from timeit import Timer
import numpy as np


# На 100 прогонов Timeit - 12.8689 c
def unoptimized_func():
    """Неоптимизированный вариант из задания"""
    numbers = [i for i in range(1, 1000001)]
    squares = []
    for number in numbers:
        squares.append(number ** 2)

# На 100 прогонов Timeit - 8.6707 c
def optimized_func():
    """Оптимизированный вариант из задания"""
    squares = [i ** 2 for i in range(1, 1000001)]

# Выполняется моментально, так как только создается объект генератора)
def generator():
    """Если условия позволяют, то лучше хранить в виде генератора"""
    squares = (i ** 2 for i in range(1, 1000001))

# На 100 прогонов Timeit - 0.4038 c
def numpy_func():
    """Самый шустрый вариант - NumPy массив."""
    numbers = np.arange(1, 1000001)
    squares = numbers ** 2



print('Unoptimized ', Timer(unoptimized_func).timeit(number=100))
print('Optimized ', Timer(optimized_func).timeit(number=100))
print('Numpy ', Timer(numpy_func).timeit(number=100))
