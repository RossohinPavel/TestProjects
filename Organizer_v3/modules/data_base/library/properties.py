"""
    Содержит описание свойств продуктов, которые представлены в виде функций.
    Функции возвращают возможные для этого свойства значения в виде кортежа. 
"""

def __zero_return() -> tuple[int]:
    """Заглушка, для возврата 0"""
    return 0,


def name() -> tuple[str, ...]:
    """Имя продукта"""
    return ('Новый продукт', )


def type() -> tuple[str, ...]:
    """Типы продукта"""
    return (
        'Фотоальбом', 'Фотоальбом Пур', 'FlexBind',
        'Фотохолст',
        'Фотожурнал',
        'Layflat',
        'Фотокнига', 'ЛЮКС',
        'Фотопапка',
        'Субпродукт'
    )


def segment() -> tuple[str, ...]:
    """Сегмент продукции"""
    return ('Премиум', 'Тираж')


def short_name() -> tuple[str, ...]:
    """Короткие имена продуктов"""
    return (
        'ПА', 'ПУР', 'ФБ', 
        'Журнал',
        'ППК', 'ПК',
        'КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС',
        'Дуо', 'Дуо гор', 'Трио',
        '+полигр фото', '+открытки', '+магниты', '+холсты'
    )


def format() -> tuple[str, ...]:
    """Форматы продуктов"""
    return (
        '10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в',                # Форматы для книжной продукции
        '30x20г', '25x25', '30x30', '40x30г', '30x40в', '32х45',
        '30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз',      # Форматы фотохолстов
        '45x45', '50x50', '50x75 верт', '50x75 гориз', '60x60', '60x90 верт', 
        '60x90 гориз', '80x80', '80x120 верт', '80x120 гориз'
    )


def cover_type() -> tuple[str, ...]:
    """Типы сборки обложки"""
    return'Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка'


carton_length = __zero_return
carton_height = __zero_return
cover_flap = __zero_return
cover_joint = __zero_return


def __print_mat() -> tuple[str, ...]:
    """Общая ф-я печатного материала"""
    cvr_photo = ('Fuji CA Matte 203x406', 'Fuji CA Matte 203x500', 'Fuji CA Matte 203x570', 'Fuji CA Matte 254x400',
                    'Fuji CA Matte 254x470', 'Fuji CA Matte 254x500', 'Fuji CA Matte 254x620', 'Fuji CA Matte 254x700',
                    'Fuji CA Matte 254x770', 'Fuji CA Matte 305x600', 'Fuji CA Matte 305x675')
    cvr_poly = ('Omela 500', 'Omela 700', 'Raflatac 500', 'Raflatac 700')
    pg_photo = ('Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305', 'Fuji CA Matte 203x400',
                'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512', 'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402',
                'Fuji CA Matte 305x610', 'Fuji CA Matte 305x810')
    pg_poly = ('Sappi SRA3', 'Sappi 320x620', 'UPM SRA4 150', 'UPM SRA4 170', 'UPM SRA4 250', 'UPM SRA3 170',
                'UPM SRA3 250', 'Flex Bind 330x330', 'Flex Bind 320x450')
    other = ('CottonCanvas', )
    return cvr_photo + cvr_poly + pg_photo + pg_poly + other


cover_print_mat = page_print_mat = __print_mat


def __lamination() -> tuple[str, ...]:
    """Ламинация продукции"""
    return ('гля', 'мат')


cover_lam = page_lam = __lamination


def page_option() -> tuple[str, ...]:
    """Опция сборки книг"""
    return ('б/у', 'с/у', 'с/у1.2')


def dc_type() -> tuple[str, ...]:
    """Тип раскодировки"""
    return 'Альбом', 'Журнал', 'Комбинация страниц'

dc_top_indent = __zero_return
dc_left_indent = __zero_return
dc_overlap = __zero_return