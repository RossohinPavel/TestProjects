from ._handler import *


class CoverMarkerHandler(Handler):
    __slots__ = '__name__', 'proxy', 'source', 'destination', 'middle_path'
    grabber_mode = 'Exemplar', 'Constant'

    def get_processing_frame_header(self) -> str:
        return f'Разметка обложек в заказе {self.proxy.name}'

    def get_total_sum_of_images(self) -> int:
        count = 0
        for i, f_g in enumerate(self.proxy.files):
            if self.proxy.content[i].comp in ('Копии', 'О_О', None):
                count += 1
            else:
                count += len(tuple(f_g.covers_from_ex_iter()))
        return count

    def handler_run(self, product, file_grabber, kwargs):
        # Формируем путь, куда будут сохранятся обложки и создаем соответствующую папку.
        save_place = f'{self.destination}/{self.middle_path}/{kwargs["edt_name"]}/{"Constant" if kwargs["comp"] in ("Копии", "О_О") else "Covers"}'
        os_makedirs(save_place, exist_ok=True)
        # Получаем настройки продукта. Значения, которые указаны в мм, переводим в пиксельные.
        kwargs['cover_type'] = product.cover_type
        kwargs['book_option'] = getattr(product, 'book_option', None)
        kwargs['clapan'] = self.mm_to_pixel(product.cover_clapan)
        kwargs['carton_len'] = self.mm_to_pixel(product.carton_length)
        kwargs['joint'] = self.mm_to_pixel(product.cover_joint)
        # Получаем генератор для итерации по обложкам исходя из типа совмещения
        cover_iter = file_grabber.cover_from_constant_iter if kwargs["comp"] in ('Копии', 'О_О') else file_grabber.covers_from_ex_iter
        for ex, cover_name, ex_len in cover_iter():
            # Записываем в словарь имя обложки и количество разворотов
            kwargs['cover_name'], kwargs['ex_len'] = cover_name, ex_len
            # Выводим строку статуса обработки
            self.storage.pf.status.set(f'{self.storage.pf.pb["value"] + 1}/{self.storage.pf.pb["maximum"]} {cover_name} -- {kwargs["edt_name"]}')
            # Считываем длинну и высоту обложки, на основе которой будет размечаться задняя часть.
            with Image.open(f'{self.source}/{self.middle_path}/{kwargs["edt_name"]}/{ex}/{cover_name}') as cover_img:
                kwargs['cover_width'], kwargs['cover_height'] = cover_img.width, cover_img.height
            # Создаем новый объект изображения на основе полученной ширины и высоты
            back = Image.new("RGB", (cover_img.width, cover_img.height), 'white')
            back_draw = ImageDraw.Draw(back)
            # Пропускаем объект через функции для обработки
            self.mark_carton(back_draw, **kwargs)
            self.mark_spine(back_draw, **kwargs)
            if kwargs['handler_option']:
                self.paste_backprint(back_draw, **kwargs)
            # Сохраняем изображение
            back.save(f'{save_place}/{cover_name[:-4]}_1.jpg', quality=100, dpi=(300, 300))
            self.storage.pf.pb["value"] += 1

    @staticmethod
    def mark_carton(back_draw, **kwargs):
        """Разметка картонок для задней части обложки"""
        back_draw.rectangle(
            (kwargs['clapan'], kwargs['clapan'],
             kwargs['clapan'] + kwargs['carton_len'], kwargs['cover_height'] - kwargs['clapan']
             ),
            outline='#000000')
        back_draw.rectangle(
            (kwargs['cover_width'] - kwargs['clapan'], kwargs['clapan'],
             kwargs['cover_width'] - kwargs['clapan'] - kwargs['carton_len'], kwargs['cover_height'] - kwargs['clapan']
             ),
            outline='#000000')

    @staticmethod
    def mark_spine(back_draw, **kwargs):
        """Разметка корешка для задней части обложки"""
        main = kwargs['clapan'] + kwargs['carton_len']
        if kwargs['cover_type'] == 'Книга':
            main = main + kwargs['joint']
        back_draw.rectangle(
            (main, kwargs['clapan'],
             kwargs['cover_width'] - main, kwargs['cover_height'] - kwargs['clapan']
             ),
            outline='#000000')
        if kwargs['cover_type'] == 'Книга':
            back_draw.rectangle(
                (main, kwargs['clapan'] + 99,
                 kwargs['cover_width'] - main, kwargs['cover_height'] - kwargs['clapan'] - 99
                 ),
                fill='#FFFFFF')

    @staticmethod
    def paste_backprint(back_draw, **kwargs):
        """Отрисовка бэкпринта на обложке"""
        text = f'{kwargs["order"]}/{kwargs["edt_name"][:20]}.../{kwargs["cover_name"]} -- {kwargs["ex_len"]}p'
        book_option = kwargs['book_option']
        if book_option:
            text += f' {book_option}'
        back_draw.text((5 + kwargs['cover_width'] - kwargs['clapan'] - kwargs['carton_len'], kwargs['clapan']),
                       text=text, font=ImageFont.truetype("arial.ttf", 60), fill="gray")
