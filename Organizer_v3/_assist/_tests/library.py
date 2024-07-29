from sys import path as sys_path
from os import name as os_name


match os_name:
    case 'nt':
        sys_path.insert(0, __file__.rsplit('\\', maxsplit=3)[0])
    case 'posix' | _:
        sys_path.insert(0, __file__.rsplit('/', maxsplit=3)[0])


from modules.data_base.library.products import *


def product_test(*products) -> None:
    """Тестирование конструктора продуктов на полноту генерируемых категорий"""
    for product in products:     # Проверяем на присутсвие атрибутов
        name = product.__name__
        # Общие тесты
        assert 'name' in product._fields, f'Отсутствует атрибут для указания названия в {name}'
        assert 'segment' in product._fields, f'Отсутствует атрибут сегмента продукции в {name}'
        assert 'short_name' in product._fields, f'Отсутствует атрибут списока коротких имен в {name}'
        # Формат книг
        if name in ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Canvas'):
            assert 'product_format' in product._fields, f'Отсутствует атрибут формата продукта в {name}'
        # Утолщение
        if name in ('Photobook', 'Layflat'):
            assert 'book_option' in product._fields, f'Отсутствует атрибут утолщения продукта в {name}'
        # Ламинация
        if name in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            assert 'lamination' in product._fields, f'Отсутствует атрибут указания ламинации в {name}'
        # Тип оболожки
        if name in ('Photobook', 'Layflat', 'Album'):
            assert 'cover_type' in product._fields, f'Отсутствует атрибут списка типов обложки в {name}'
        # Размер Картонки
        if name in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            assert 'carton_length' in product._fields, f'Отсутствует указание длинны картона в {name}'
            assert 'carton_height' in product._fields, f'Отсутствует указание высоты картона в {name}'
        # Клапан и шарнир
        if name in ('Photobook', 'Layflat', 'Album'):
            assert 'cover_flap' in product._fields, f'Отсутствует указание значений клапана в {name}'
            assert 'cover_joint' in product._fields, f'Отсутствует указание значений шарнира в {name}'
        # Печатный материал обложек
        assert 'cover_print_mat' in product._fields, f'Отсутствует cписок печатного материала обложек в {name}'
        # Печатный материал разворотов
        if name in ('Photobook', 'Layflat', 'Album', 'Journal'):
            assert 'page_print_mat' in product._fields, f'Отсутствует печатного материала разворота в {name}'
        # """Частные тесты продуктов"""
        if name == 'Photobook':
            assert 'cover_canal' in product._fields
            assert 'page_canal' in product._fields
        if name == 'Album':
            assert 'dc_break' in product._fields
            assert 'dc_overlap' in product._fields
            assert 'dc_top_indent' in product._fields
            assert 'dc_left_indent' in product._fields


if __name__ == '__main__':
    product_test(Album, Canvas, Journal, Layflat, Photobook, Photofolder, Subproduct)
    print('Succes!')
