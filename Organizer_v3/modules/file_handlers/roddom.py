import os
from shutil import copy2 as sh_copy2
from re import search
import modules.app_manager as APP


class RoddomHandler:
    __slots__ = 'path', 'order', '__make_txt', '__img_len'

    def __init__(self, path: str, make_txt=True):
        self.__make_txt = make_txt
        self.__img_len = 0
        self.path, self.order = path.rsplit('/', 1)

    def get_calc_info(self) -> dict:
        """Получение информации о заказе"""
        dct = {'9x15': 0, '15x21': 0, '21x30': 0}
        for path, files in self.__walk_on_order():
            dct[os.path.split(path)[-1]] += len(files)
        if self.__make_txt:
            with open(f'{self.path}/{self.order}/sum.txt', 'w', encoding='utf-8') as file:
                print(*(f'{k}: {v}' for k, v in dct.items()), sep='\n', file=file)
        self.__img_len = sum(dct.values())
        return dct

    def __walk_on_order(self):
        """Генераторная ф-я для пробега по файлам заказа"""
        for root in os.walk(f'{self.path}/{self.order}'):
            rel_path = root[0].removeprefix(self.path)
            if search(r'\d{1,2}x\d{2}', rel_path):
                yield rel_path, root[-1]
    
    @APP.THREAD_MANAGER.in_queue
    def to_print(self, path: str) -> None:
        """Отправка в печать (копирование файлов в указанную папку)"""
        APP.pf.header.step(f'Роддом: {self.order}')
        APP.pf.operation.step('Копирование на печать')

        APP.pf.filebar.maximum(self.__img_len)

        for rel_path, files in self.__walk_on_order():
            new_path = f'{path}/{rel_path}'
            os.makedirs(new_path, exist_ok=True)
            for file in files:
                APP.pf.filebar.step(file)
                sh_copy2(f'{self.path}/{rel_path}/{file}', f'{new_path}/{file}')
                APP.pf.filebar.step_end()
