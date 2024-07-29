import os
from tkinter import filedialog as tkfd


SYMBOLS = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
           'ё': 'e', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k',
           'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
           'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
           'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '',
           'э': 'e', 'ю': 'yu', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V',
           'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'J', 'З': 'Z',
           'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
           'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
           'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SH',
           'Ъ': '', 'Ы': 'I', 'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA'}

def transliterating(string: str) -> str:
    new_name = ''
    for i in string:
        if i.isdigit():
            new_name += i
        else:
            new_i = SYMBOLS.get(i)
            new_name += new_i if new_i else i
    return new_name


def dir_enumerating(path: str):
    """Перебор директорий и отправка имени папки на транслитерацию"""
    for root, dirs, files in os.walk(path, topdown=False):
        for catalog in dirs:
            src = os.path.join(root, catalog)
            dst = os.path.join(root, transliterating(catalog))
            os.rename(src, dst)


if __name__ == '__main__':
    path = tkfd.askdirectory(title='Укажите папку, где нужно заменить символы')
    if path:
        dir_enumerating(path)
