"""
    Содержит 'дескрипторы' - объекты, которые хранят
    некоторую информацию и могут вызывать связанные с 
    ними функции, помещая в них это значение.
"""
from typing import Callable, Generic, TypeVar


__all__ = ('autolog', 'log_check_depth', 'z_disc', 'o_disc', 't_disc', 'roddom_dir', 'theme', 'color')


T = TypeVar('T')


class DescriptorConstructor(Generic[T]):
    """
        Класс, реализующий логику работы дескриптора.
        Помимо этого, при получении значения, вызывает
        связанные функции из _funcs.
    """

    __slots__ = '_value', '_funcs'

    def __init__(self):
        self._value: T = None   #type: ignore
        self._funcs = ()

    def __get__(self, *_) -> T:
        return self._value

    def __set__(self, _, value: T) -> None:
        self._value = value
        for func in self._funcs: func(value)

    def add_call(self, func: Callable[[T], None]) -> None:
        """Добавление функции в коллекцию вызовов"""
        self._funcs += (func, )


# Дескрипторы настроек. Они импортируются по *
autolog = DescriptorConstructor[int]()
log_check_depth = DescriptorConstructor[int]()
z_disc = DescriptorConstructor[str]()
o_disc = DescriptorConstructor[str]()
t_disc = DescriptorConstructor[str]()
roddom_dir = DescriptorConstructor[str]()
theme = DescriptorConstructor[str]()
color = DescriptorConstructor[str]()

# Остальные дескрипторы
ot_status = DescriptorConstructor[str]()
