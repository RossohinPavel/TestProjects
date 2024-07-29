from PIL import Image, ImageDraw, ImageFont
import shutil


def album_decoding(file_list: tuple, ex_src: str, ex_dest: str, ex):
    pages_count = 1
    with Image.open(f'{ex_src}/{file_list[0]}') as image_to_meas:
        image_to_meas.load()
    len_x = image_to_meas.width
    len_y = image_to_meas.height
    len_x_even = int(len_x / 2 + 95)
    len_x_uneven = int(len_x / 2 - 95)
    image_to_meas.close()
    white_image = Image.new('RGB', (len_x_even, len_y), 'white')
    white_image.save(f'{ex_dest}/{ex}__page{pages_count}.jpg', quality=100, dpi=(300, 300))
    pages_count += 1
    for name in file_list:
        with Image.open(f'{ex_src}/{name}') as page_image:
            page_image.load()
        l_side = page_image.crop((0, 0, len_x_even, len_y))
        r_side = page_image.crop((len_x_uneven, 0, len_x, len_y))
        l_side.save(f'{ex_dest}/{ex}__page{pages_count}.jpg', quality=100, dpi=(300, 300))
        pages_count += 1
        r_side.save(f'{ex_dest}/{ex}__page{pages_count}.jpg', quality=100, dpi=(300, 300))
        pages_count += 1
    white_image.save(f'{ex_dest}/{ex}__page{pages_count}.jpg', quality=100, dpi=(300, 300))


def journal_decoding(file_list: tuple, ex_src: str, ex_dest: str):
    file_list_len = len(file_list)
    if file_list_len % 2 == 0:
        even_count = file_list_len - 2
        uneven_count = 1
        cover = file_list[-1]
        shutil.copy2(f'{ex_src}/{cover}', f'{ex_dest}/br000.jpg')
        pages = file_list[:-1:]
        for name in pages:
            l_index = pages.index(name)
            r_index = -1 - l_index
            with Image.open(f'{ex_src}/{pages[l_index]}') as l_image:
                l_image.load()
            len_x = int(l_image.width / 2)
            len_y = l_image.height
            l_image_crop = l_image.crop((0, 0, len_x, len_y))
            l_image.close()
            with Image.open(f'{ex_src}/{pages[r_index]}') as r_image:
                r_image.load()
            r_image.paste(l_image_crop)
            if pages[l_index] <= pages[r_index]:
                file_name = f'br{str(uneven_count).rjust(3, "0")}.jpg'
                uneven_count += 2
            else:
                file_name = f'br{str(even_count).rjust(3, "0")}.jpg'
                even_count -= 2
            r_image.save(f'{ex_dest}/{file_name}', quality='keep', dpi=(300, 300))
    else:
        pass


def cover_processing(file_source: str, file_dest: str, **kwargs):
    with Image.open(file_source) as cover_image:
        cover_image.load()
    draw = ImageDraw.Draw(cover_image)
    rec_x = cover_image.width
    rec_y = cover_image.height
    # Прорисовка обводки
    stroke_color = kwargs['s_color'] if 's_color' in kwargs else '#000000'
    stroke_size = kwargs['s_size'] if 's_size' in kwargs else 4
    if 's_color' in kwargs and 's_size' in kwargs:
        draw.rectangle((0, 0, rec_x, rec_y), outline=stroke_color, width=stroke_size)
    # Направляющие для обычных книг
    gl_color = kwargs['gl_color'] if 'gl_color' in kwargs else '#000000'
    gl_size = kwargs['gl_size'] if 'gl_size' in kwargs else 4
    gl_spine = kwargs['gl_spine'] if 'gl_spine' in kwargs else 0
    file_name = kwargs['file_name'] if 'file_name' in kwargs else '0.jpg'
    if gl_spine > 0 and kwargs['luxe'] is False:
        draw.line((gl_spine, 0, gl_spine, 90), fill=gl_color, width=gl_size)
        draw.line((rec_x - gl_spine, 0, rec_x - gl_spine, 90), fill=gl_color, width=gl_size)
        draw.line((gl_spine, rec_y, gl_spine, rec_y - 90), fill=gl_color, width=gl_size)
        draw.line((rec_x - gl_spine, rec_y, rec_x - gl_spine, rec_y - 90), fill=gl_color, width=gl_size)
    # Направляющие для Люкс книг
    if gl_spine > 0 and kwargs['luxe'] is True:
        draw.line((gl_spine, 0, gl_spine, rec_y), fill=gl_color, width=gl_size)
        draw.line((gl_spine + 590, 0, gl_spine + 590, 60), fill=gl_color, width=gl_size)
        draw.line((rec_x - gl_spine - 590, 0, rec_x - gl_spine - 590, 60), fill=gl_color, width=gl_size)
        draw.line((gl_spine + 590, rec_y, gl_spine + 590, rec_y - 60), fill=gl_color, width=gl_size)
        draw.line((rec_x - gl_spine - 590, rec_y, rec_x - gl_spine - 590, rec_y - 60), fill=gl_color, width=gl_size)
        draw.line((rec_x - gl_spine, 0, rec_x - gl_spine, rec_y), fill=gl_color, width=gl_size)
    # Бек принт
    if 'back_print' in kwargs:
        # Рисуем задник для бекпринта
        new_name = kwargs['back_print']
        back_print = Image.new('RGB', (len(new_name) * 21, 50), 'white')
        # Определяем объект для текста
        draw_text = ImageDraw.Draw(back_print)
        # Получаем шрифт
        font = ImageFont.truetype("Data\\Settings\\Roboto-Regular.ttf", size=40)
        # Рисуем текст на заднике
        draw_text.text((20, 0), text=new_name, font=font, fill="black")
        # Поворачиваем задник
        rotated_back_print = back_print.rotate(90, expand=True)
        # Получаем размеры бекпринта
        bp_x = back_print.width
        bp_y = back_print.height
        # Вставляем бэкпринт на исходное изображение
        bp_pos_x = rec_x - kwargs['gl_spine'] + 10 if 'gl_spine' in kwargs else int(rec_x / 2) + 10
        cover_image.paste(back_print, (bp_pos_x, rec_y - bp_y))
        cover_image.paste(rotated_back_print, (rec_x - bp_y, int((rec_y / 2) - (bp_x / 2))))
    cover_image.save(f'{file_dest}/{file_name}', quality='keep', dpi=(300, 300))
