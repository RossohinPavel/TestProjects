__all__ = ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Canvas', 'Subproduct')

SEGMENT = ['Премиум', 'Тираж']

PRODUCTFORMAT = ['10x10', "15x15", "15x20в", "20x15г", "20x20", "20x30в", "30x20г", "25x25", "30x30", "40x30г",
                 "30x40в"]

BOOKOPTION = ["б/у", "с/у", "с/у1.2"]

COVERCARTON = ['145x205', '145х153', '153x205', '193x153', '193x205', '193x300', '200x153', '200x205', '200x300',
               '248x255', '255x255', '293x205', '293x300', '300x205', '300x300']

COVERTYPE = ['Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка']

CANVASFORMAT = ['30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50', '50x75 верт',
                '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80', '80x120 верт', '80x120 гориз']

PHOTOCOVERMATERIAL = ['Fuji CA Matte 152x204', 'Fuji CA Matte 152x304', 'Fuji CA Matte 152x370',
                      'Fuji CA Matte 203x305', 'Fuji CA Matte 203x406', 'Fuji CA Matte 203x470',
                      'Fuji CA Matte 203x500', 'Fuji CA Matte 203x570', 'Fuji CA Matte 254x400',
                      'Fuji CA Matte 254x470', 'Fuji CA Matte 254x500', 'Fuji CA Matte 254x620',
                      'Fuji CA Matte 254x700', 'Fuji CA Matte 254x770', 'Fuji CA Matte 305x610',
                      'Fuji CA Matte 305x675']

PHOTOPAGEMATERIAL = ['Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305', 'Fuji CA Matte 203x400',
                     'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512', 'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402',
                     'Fuji CA Matte 305x610', 'Fuji CA Matte 305x810']

COVERCANAL = ['160', '161', '162', '163', '164', '165', '166', '204', '205', '214', '240', '242', '243', '245', '266',
              '36', 'ORAJET', 'POLI']

PAGECANAL = ['201', '214', '203', '204', '205', '207', '275', '274', '276', '271']

POLYGRAPHICCOVERMATERIAL = ["Omela 500", "Omela 700", "Raflatac 500", "Raflatac 700"]

POLYGRAPHICPAGEMATERIAL = ["Sappi SRA3", "Sappi 320x620", "UPM SRA4 170", "UPM SRA4 150", "UPM SRA4 250",
                           "UPM SRA3 170", "UPM SRA3 250", "Flex Bind 330x330", "Flex Bind 320x450"]

LAMINATION = ['гля', 'мат']


class Product:
    """Абстрактный класс для описания продукта. Содержит обязательные атрибуты для всех продуктов"""

    def __init__(self):
        self.full_name = ''
        self.segment = []
        self.short_name = []
        self.cover_print_mat = []

    def get_descr_to_sqldb(self) -> dict:
        """Получение списка атрибутов и типов их значений для создания sql базы данных"""
        dct = {}
        for key, value in self.__dict__.items():
            if type(value) == list:
                value = value[0]
            dct.update({key: 'TEXT' if type(value) == str else 'INTEGER'})
        return dct


class Photobook(Product):
    """Описание атрибутов фотокниг на фотобумаге"""
    name = "Фотокниги на Фотобумаге"
    category = 'photobook'

    def __init__(self):
        super().__init__()
        self.segment = SEGMENT
        self.short_name = ["КС", "Люкс", "кКожа", "КК", "ПС"]
        self.product_format = PRODUCTFORMAT
        self.book_option = BOOKOPTION
        self.lamination = LAMINATION
        self.cover_print_mat = PHOTOCOVERMATERIAL + POLYGRAPHICCOVERMATERIAL[:2]
        self.cover_carton = COVERCARTON
        self.page_print_mat = PHOTOPAGEMATERIAL
        self.cover_type = COVERTYPE
        self.gl_pos = 0
        self.gl_len = 0
        self.cover_canal = COVERCANAL
        self.page_canal = PAGECANAL


class Layflat(Product):
    """Описание атрибутов полиграфических книг Layflat"""
    name = 'Полиграфические фотокниги Layflat'
    category = 'layflat'

    def __init__(self):
        super().__init__()
        self.segment = SEGMENT
        self.short_name = ["ППК", "ПК"]
        self.product_format = PRODUCTFORMAT
        self.book_option = BOOKOPTION
        self.lamination = LAMINATION
        self.cover_print_mat = POLYGRAPHICCOVERMATERIAL
        self.cover_carton = COVERCARTON
        self.page_print_mat = POLYGRAPHICPAGEMATERIAL
        self.cover_type = COVERTYPE[:2]
        self.gl_pos = 0
        self.gl_len = 0


class Album(Product):
    """Описание атрибутов полиграфических альбомов, ПУР и Флексбайнд книг"""
    name = 'Полиграфические альбомы, PUR, FlexBind'  # Русское имя сегмента продукции
    category = 'album'

    def __init__(self):
        super().__init__()
        self.segment = SEGMENT
        self.short_name = ["ФБ", "ПА", "ПУР"]
        self.product_format = PRODUCTFORMAT
        self.lamination = LAMINATION
        self.cover_print_mat = POLYGRAPHICCOVERMATERIAL
        self.cover_carton = COVERCARTON
        self.page_print_mat = POLYGRAPHICPAGEMATERIAL
        self.cover_type = COVERTYPE[:1]
        self.gl_pos = 0
        self.gl_len = 0
        self.dc_break = 0
        self.dc_overlap = 0
        self.dc_top_indent = 0
        self.dc_left_indent = 0


class Journal(Product):
    """Описание атрибутов полиграфического фотожурнала"""
    name = 'Полиграфические фотожурналы'  # Русское имя сегмента продукции
    category = 'journal'

    def __init__(self):
        super().__init__()
        self.segment = SEGMENT[1:2]
        self.short_name = ['Журнал']
        self.product_format = ["20x30в", '20х20']
        self.cover_print_mat = POLYGRAPHICPAGEMATERIAL
        self.page_print_mat = POLYGRAPHICPAGEMATERIAL


class Photofolder(Product):
    """Описание атрибутов полиграфических фотопапок"""
    name = 'Фотопапки'  # Русское имя сегмента продукции
    category = 'photofolder'

    def __init__(self):
        super().__init__()
        self.segment = SEGMENT[1:2]
        self.short_name = ["Дуо", "Дуо гор", "Трио"]
        self.product_format = ["20x30в", "30x20г"]
        self.lamination = LAMINATION
        self.cover_print_mat = POLYGRAPHICCOVERMATERIAL
        self.cover_carton = ["200x300 2.0"]


class Canvas(Product):
    """Описание атрибутов фотохолстов"""
    name = 'Фотохолсты'  # Русское имя сегмента продукции
    category = 'canvas'

    def __init__(self):
        super().__init__()
        self.segment = SEGMENT[:1]
        self.short_name = ["+холсты"]
        self.product_format = CANVASFORMAT
        self.cover_print_mat = ['CottonCanvas']


class Subproduct(Product):
    """Описание атрибутов всех остальных продуктов"""
    name = 'Остальное'
    category = 'subproduct'

    def __init__(self):
        super().__init__()
        self.segment = SEGMENT[1:2]
        self.short_name = ["+полигр фото", '+открытки']
        self.cover_print_mat = POLYGRAPHICPAGEMATERIAL + PHOTOCOVERMATERIAL


def test():
    obj_lst = [Photobook(), Layflat(), Album(), Journal(), Photofolder(), Canvas(), Subproduct()]
    for obj in obj_lst:
        # """Общие тесты"""
        assert obj.__class__.name != '', f'Пропущенно русское имя категории продукции в {obj.__class__}'
        assert 'full_name' in obj.__dict__
        assert obj.__dict__['segment'] != [], f'Отсутствует указание сегмента продукции в {obj.__class__}'
        assert obj.__class__.category != '', f'Отсутствует указание категории продукции в {obj.__class__}'
        assert obj.__dict__['short_name'] != [], f'Отсутствует список коротких имен в {obj.__class__}'
        assert obj.__dict__[
                   'cover_print_mat'] != [], f'Отсутствует cписок печатного материала обложек в {obj.__class__}'
        # Формат книг
        if type(obj) in (Photofolder, Canvas, Journal, Album, Layflat, Photobook):
            assert 'product_format' in obj.__dict__ and obj.__dict__[
                'product_format'] != [], f'Отсутствует указание формата продукта в {obj.__class__}'
        # Утолщение
        if type(obj) in (Layflat, Photobook):
            assert 'book_option' in obj.__dict__ and obj.__dict__[
                'book_option'] != [], f'Отсутствует указание утолщения продукта в {obj.__class__}'
        # Ламинация
        if type(obj) in (Photofolder, Album, Layflat, Photobook):
            assert 'lamination' in obj.__dict__ and obj.__dict__[
                'lamination'] != [], f'Отсутствует указаybt ламинации в {obj.__class__}'
        # Картон обложечный
        if type(obj) in (Photofolder, Album, Layflat, Photobook):
            assert 'cover_carton' in obj.__dict__ and obj.__dict__[
                'cover_carton'] != [], f'Отсутствует обложечного картона в {obj.__class__}'
        # Печатный материал разворотов
        if type(obj) in (Journal, Album, Layflat, Photobook):
            assert 'page_print_mat' in obj.__dict__ and obj.__dict__[
                'page_print_mat'] != [], f'Отсутствует печатного материала разворота в {obj.__class__}'
        # тип оболожки
        if type(obj) in (Album, Layflat, Photobook):
            assert 'cover_type' in obj.__dict__ and obj.__dict__[
                'cover_type'] != [], f'Отсутствует указание списка типов обложки в {obj.__class__}'
        # Позиция направляющих
        if type(obj) in (Album, Layflat, Photobook):
            assert 'gl_pos' in obj.__dict__, f'Отсутствует атрибут позиции направляющих {obj.__class__}'
        # Длинна направляющих
        if type(obj) in (Album, Layflat, Photobook):
            assert 'gl_len' in obj.__dict__, f'Отсутствует атрибут длинны направляющих {obj.__class__}'
        # """Частные тесты продуктов"""
        if isinstance(obj, Photobook):
            assert 'cover_canal' in obj.__dict__
            assert 'page_canal' in obj.__dict__
        if isinstance(obj, Album):
            assert 'dc_break' in obj.__dict__
            assert 'dc_overlap' in obj.__dict__
            assert 'dc_top_indent' in obj.__dict__
            assert 'dc_left_indent' in obj.__dict__
        if isinstance(obj, Canvas):
            assert obj.__dict__['product_format'] == CANVASFORMAT


if __name__ == '__main__':
    test()
    print(sorted(PHOTOPAGEMATERIAL))