from ._handler import *
from os import listdir as os_listdir, rename as os_rename
from shutil import rmtree


class PageDecoder(Handler):
    __slots__ = '__name__', 'proxy', 'source', 'destination', 'middle_path'
    grabber_mode = 'Exemplar', 'Constant'

    def get_processing_frame_header(self) -> str:
        return f'Раскодировка разворотов в заказе {self.proxy.name}'

    def get_total_sum_of_images(self) -> int:
        count = 0
        for i, f_g in enumerate(self.proxy.files):
            cover_included = False
            comp_tuple = ('Копии', )
            if self.proxy.products[i].category == 'Album':
                comp_tuple += ('В_О', )
            else:
                cover_included = True
            for ex, pages in f_g.pages_from_ex_iter(self.proxy.content[i].comp in comp_tuple, cover_included):
                count += sum(1 for _ in pages)
        return count

    def handler_run(self, product, file_grabber, kwargs):
        # Формируем пути, которые будут использоваться в раскодировщиках
        edt_path = f'{self.middle_path}/{kwargs["edt_name"]}'
        destination_path = f'{self.destination}/{edt_path}/Pages'
        os_makedirs(destination_path, exist_ok=True)
        kwargs['src_path'], kwargs['dst_path'] = f'{self.source}/{edt_path}', destination_path
        # Распределяем тиражи по соответствующим функциям
        if product.category == 'Journal':
            self.journal_decoder(product, file_grabber, kwargs)
        if product.category == 'Album':
            # Оборачиваем нужные атрибуты в пиксельные значения
            kwargs['dc_overlap'] = m_ceil(self.mm_to_pixel(product.dc_overlap))
            kwargs['dc_top_indent'] = m_ceil(self.mm_to_pixel(product.dc_top_indent))
            kwargs['dc_left_indent'] = m_ceil(self.mm_to_pixel(product.dc_left_indent))
            self.album_decoder(product, file_grabber, kwargs)
            if product.dc_break:
                self.break_decoder(kwargs)

    def journal_decoder(self, product, file_grabber, kwargs):
        pass

    @staticmethod
    def __create_stub_image(path, text=None):
        """Создает и возвращает белое изображение, которое используется для заглушки"""
        white_image = Image.new('RGB', (2400, 2400), 'white')
        if text:
            draw_text = ImageDraw.Draw(white_image)
            draw_text.text((235, 2125), text=text, fill="#C0C0C0", font=ImageFont.truetype("arial.ttf", 80))
        white_image.save(path, quality=100, dpi=(300, 300))

    @staticmethod
    def __get_decoded_album_pages(path, kwargs):
        """Открывает изображение, кропает его и возвращает получившиеся стороны"""
        with Image.open(path) as image:
            image.load()
        # Кропаем поступившие изображения
        l_side = image.crop((0, 0, image.width // 2 + kwargs['dc_overlap'], image.height))
        # Создаем новый задник
        new_l_side = Image.new('RGB', (l_side.width + kwargs['dc_left_indent'], l_side.height + kwargs['dc_left_indent']), 'white')
        # Вставляем Левую сторону на новый задник
        new_l_side.paste(l_side, (0, kwargs['dc_top_indent']))
        l_side.close()
        yield new_l_side
        # Повторяем с правой стороной зеркально
        r_side = image.crop((image.width // 2 - kwargs['dc_overlap'], 0, image.width, image.height))
        image.close()
        new_r_side = Image.new('RGB', (r_side.width + kwargs['dc_left_indent'], r_side.height + kwargs['dc_top_indent']), 'white')
        new_r_side.paste(r_side, (kwargs['dc_left_indent'], kwargs['dc_top_indent']))
        yield new_r_side

    def album_decoder(self, product, file_grabber, kwargs):
        """Ф-я для раскодировки альбомов и FlexBind, где не нужно комбинировать раскодированные странички"""
        cache = {}
        if kwargs['comp'] is not None: # Разметка кэша именами постоянных изображений, если в тираже больше 1 экземпляра
            for name in file_grabber.images_from_constant_iter():
                cache[name[:3]] = None
        # Итерируемся по тиражу
        for ex, imgs in file_grabber.pages_from_ex_iter(kwargs['comp'] in ('Копии', 'В_О')):
            imgs = tuple(imgs)
            # Создаем переменные зависимые от настройки обработчика
            ex_name, text = ex, None
            if kwargs['handler_option']:
                ex_name, text = f'{len(imgs)}p_{ex}', f'{kwargs["order"]}/{kwargs["edt_name"][:25]}/{ex}'
            # Создаем каталог для экземпляра
            dst_path = f'{kwargs["dst_path"]}/{ex_name}'
            os_makedirs(dst_path, exist_ok=True)
            # Создаем верхнюю заглушку
            page_count = 1
            self.__create_stub_image(f'{dst_path}/page{page_count}.jpg', text)
            page_count += 1
            # Итерируемся по изображениям
            for spread in imgs:
                self.storage.pf.status.set(f'{self.storage.pf.pb["value"] + 1}/{self.storage.pf.pb["maximum"]} {spread} -- {kwargs["edt_name"]}')
                spread_pos = spread[5:8]
                cropped_spreads = cache.get(spread_pos, None)
                if cropped_spreads is None:
                    cropped_spreads = self.__get_decoded_album_pages(f'{kwargs["src_path"]}/{ex}/{spread}', kwargs)
                    if spread_pos in cache:     # Записываем постоянные изображения в кэш
                        cropped_spreads = tuple(cropped_spreads)
                        cache[spread_pos] = cropped_spreads
                for page in cropped_spreads:
                    page.save(f'{dst_path}/page{page_count}.jpg', quality=100, dpi=(300, 300))
                    page_count += 1
                self.storage.pf.pb["value"] += 1
            # Создаем нижнюю заглушку
            self.__create_stub_image(f'{dst_path}/page{page_count}.jpg')

    def break_decoder(self, kwargs):
        """Ф-я для раскодировки продуктов с комбинированной печатью, как FlexBind 20x20"""
        cache = {x: sorted(os_listdir(f'{kwargs["dst_path"]}/{x}'), key=len) for x in os_listdir(kwargs['dst_path'])}
        self.storage.pf.pb["value"] = 0
        self.storage.pf.pb["maximum"] = len(cache)
        for ex, imgs in cache.items():
            self.storage.pf.status.set(f'{self.storage.pf.pb["value"] + 1}/{self.storage.pf.pb["maximum"]} Объединение раскодированных изображений')
            dst_path, temp = f'{kwargs["dst_path"]}/{ex}', f'{kwargs["dst_path"]}/temp'
            os_rename(dst_path, temp)
            os_makedirs(dst_path)
            if len(imgs) % 4 != 0:
                imgs.extend([imgs[-1]] * 2)
            middle = len(imgs) // 2
            for i in range(middle):
                fb_page = Image.new('RGB', (3780, 5398), 'white')
                for j, img_name in enumerate((imgs[i], imgs[middle + i])):
                    with Image.open(f'{kwargs["dst_path"]}/temp/{img_name}') as img:
                        img.load()
                        fb_page.paste(img, (0 if i % 2 == 0 else 3780 - img.width, 0 if j % 2 == 0 else 2763))
                        img.close()
                fb_page.save(f'{dst_path}/page{str(i + 1)}.jpg', quality=100, dpi=(300, 300))
                fb_page.close()
            rmtree(temp)
            self.storage.pf.pb["value"] += 1
