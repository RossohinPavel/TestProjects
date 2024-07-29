import os
import shutil
from new_modules.FileHandler import write_txt


class RoddomOrder:
    """Класс для подсчета и управления одиночным заказом роддома"""
    __slots__ = 'path', 'order_name', 'sub_lst', 'total_sum'

    def __init__(self, path, txt=False):
        self.path = path
        self.order_name = path.split('/')[-1]
        self.sub_lst = tuple(RoddomSub(path, x) for x in os.listdir(path) if os.path.isdir(f'{path}/{x}'))
        self.total_sum = self.get_total_sum()
        if txt:
            write_txt(f'{path}/{self.order_name} - sum.txt', str(self))

    def __str__(self) -> str:
        """Получение текстовой информации о заказе Роддома"""
        string = self.order_name + '\n'
        string += '\n'.join(f'{str(k).rjust(10, " ")} - {v}' for k, v in self.total_sum.items())
        return string

    def get_total_sum(self) -> dict:
        """Получение суммы отпечатков по форматам в заказе"""
        dct = {'9x15': 0, '15x21': 0, '21x30': 0}
        for sub in self.sub_lst:
            for form in sub.format_lst:
                key = str(form)
                if key not in dct:
                    dct[key] = 0
                dct[key] += len(form)
        return dct

    def create_directory(self, path: str) -> None:
        """Функция создания иерархии каталогов по новому пути, которая повторят иерархию заказа"""
        for sub in self.sub_lst:
            for format_name in sub.format_lst:
                os.makedirs(f'{path}/{self.order_name}/{sub}/{format_name}', exist_ok=True)

    def run(self, path: str) -> str:
        """Функция копирования изображений по новому пути согласно иерархии каталогов. Yield'ит имя файла"""
        for sub in self.sub_lst:
            for format_name in sub.format_lst:
                for img in format_name.img_list:
                    yield img
                    src = f'{self.path}/{sub}/{format_name}/{img}'
                    dst = f'{path}/{self.order_name}/{sub}/{format_name}/{img}'
                    shutil.copy2(src, dst)


class RoddomSub:
    """Класс для управления отдельной выпиской"""
    __slots__ = 'sub_name', 'format_lst'

    def __init__(self, path, sub):
        self.sub_name = sub
        self.format_lst = tuple(self.main(path, sub))

    @staticmethod
    def main(path, sub):
        path = f'{path}/{sub}'
        for format_name in os.listdir(path):
            if format_name in ('15x21', '21x30', '9x15'):
                yield RoddomFormat(path, format_name)

    def __str__(self):
        return self.sub_name


class RoddomFormat:
    """Класс для описания отдельных фото"""
    __slots__ = 'format_name', 'img_list'

    def __init__(self, path, format_name):
        self.format_name = format_name
        self.img_list = tuple(x for x in os.listdir(f'{path}/{format_name}') if x.endswith('.jpg'))

    def __str__(self):
        return self.format_name

    def __len__(self):
        return len(self.img_list)
