import os
import re
import time as time

import Data.config as config
import Data.get_list as get_list


class Log_creator:
    def __init__(self):
        self.daydir_list = self.__get_daydir_list()
        self.order_blank = self.__get_order_blank(self.daydir_list)
        self.ob_with_content = self.__get_content(self.order_blank)
        self.ob_with_count = self.__content_count(self.ob_with_content)
        self.ob_with_type = self.__set_content_type(self.ob_with_count)
        config.write_json_log(self.ob_with_type)

    @staticmethod
    def __get_daydir_list() -> list:
        """
        :return: Метод возвращает список папок - дней, где элемент - абсолютный путь до папки. Количество элементов
        (ограничение по дням) определяется инструкциями из Data/Settings/Settings.ini. Эти инструкции ускоряет получение
        информации для рутиной обработки заказов
        """

        # Получаем инструкции (папка сохранения заказов c сервера и ограничение по дням)

        order_dir = config.read("working_dir", "order_main_dir")
        day_limit = config.read("logs", "day_limit")

        # Формируем список папок - дней согласно инструкциям.
        # Применяем реверс для ускорения, чтобы не считывать все папки каталога.

        current_dir_list = []
        count = 0
        for name in reversed(os.listdir(order_dir)):
            # Проверяем на то, что нужная нам строчка - папка и она соответствует названию, которое присваивает сервер.

            if os.path.isdir(f"{order_dir}/{name}") and re.fullmatch(r'202\S{7}', name):
                count += 1
                if count <= int(day_limit):
                    current_dir_list.append(f"{order_dir}/{name}")
                else:
                    break
        return current_dir_list

    @staticmethod
    def __get_order_blank(daydir_list) -> dict:
        """
        :param daydir_list: Передается список путей, полученных в методе __get_daydir_list.
        :return: Метод возвращает словарь, где 1 уровень ключей - номера заказов. Сделано для удобства обращения
        пользователя. Значение для каждого ключа (заказа) - словарь с элементами PATH, CREATION_DATE, CONTENT.
        """
        # PATH получен в качестве аргумента. Получаем список папок - заказов.
        # Проверяем на то, что папка состоит из 6 символов. Получаем дату создания папки.

        orders_blank = {}
        for path in reversed(daydir_list):
            for name in os.listdir(path):
                if os.path.isdir(f"{path}/{name}") and re.fullmatch(r'\d{6}', name):
                    # Получаем и преобразуем дату создания (загрузки заказа) в читаемый формат.
                    creation_date_in_sec = os.path.getctime(f"{path}/{name}")
                    creation_date = time.strftime('%Y-%m-%d', time.strptime(time.ctime(creation_date_in_sec)))
                    # Создаем словарь для заказа и наполняем его.
                    unit_order_blank = {name: {
                        'creation_data': creation_date,
                        'path': f"{path}/{name}",
                        'content': None
                    }}
                    orders_blank.update(unit_order_blank)
        return orders_blank

    @staticmethod
    def __get_content(order_blank) -> dict:
        """
        Очищаем словарь от заказов, где контент - None
        При любом раскладе событий к значению content присоединяется заготовка словаря {type and counts}
        :param order_blank: Полученый в методе __get_order_blank пустой бланк заказов
        :return: Возвращаем дополненый словарь информацией, записанной под ключом content.
        """
        value_to_del = [] # Список значений для очистки словаря
        for name in order_blank:
            path = order_blank[name]['path']
            content_dict = {}
            for content in os.listdir(path):
                # Проверка на существование папок внутри заказов. Исключаем из записи папку "_TO_PRINT"
                if content not in ("_TO_PRINT", "TO_PRINT", "_ЕЩ_ЗКШТЕ") and os.path.isdir(f"{path}/{content}"):
                    product_dict = {content: {'counts': None, 'type': None}}
                    content_dict.update(product_dict)
            # Если удалось сформировать словарь для заказа, то прицепляем его к общему словарю. Для пустых - None
            if content_dict:
                order_blank[name]['content'] = content_dict
            else:
                value_to_del.append(name)
        # Очищаем словарь от заказов, где content - None
        for value in value_to_del:
            del order_blank[value]
        return order_blank

    @staticmethod
    def __content_count(ob_with_content) -> dict:
        """
        :param ob_with_content: Принимаем словарь с метода __get_content.
        :return: Считаем общее количества обложек и разворотов. Формируем комплексный счетчик и проверяем на совмещение.
        Возвращаем дополненый словарь
        """
        def foto_count(foto_path) -> list:
            # Метод для подсчета и типизации фотопечати Из загрузчика OB версии 2,0,0,4
            paper_format_and_count_list = []
            for photo_paper in os.listdir(f"{foto_path}/_ALL/Фотопечать"):
                paper_type = ""      # Определяем тип бумаги и записываем в переменную
                photo_dict = {}
                if photo_paper == "Глянцевая":
                    paper_type = "Fuji GL"
                elif photo_paper == "Матовая":
                    paper_type = "Fuji MT"
                elif photo_paper == "Silk":
                    paper_type = "Fuji Silk"
                for photo_format in os.listdir(f"{foto_path}/_ALL/Фотопечать/{photo_paper}"):
                    # Разделяем имя папки на формат и мультипликатор (используется для подсчета)
                    photo_name, multiplier = photo_format.split("--")
                    path_to_list = os.listdir(f"{foto_path}/_ALL/Фотопечать/{photo_paper}/{photo_format}")
                    photo_count = len(path_to_list) * int(multiplier)
                    format_name = photo_name.split(" ")[1]
                    value_to_add = (f"{paper_type} {format_name}", photo_count)
                    if value_to_add[0] in photo_dict:
                        photo_dict[value_to_add[0]] += value_to_add[1]
                    else:
                        photo_dict.update({f"{value_to_add[0]}": value_to_add[1]})
                paper_format_and_count_list.append(photo_dict)
            return paper_format_and_count_list


        def count_fx(ex_list):
            long_list = []
            # Формируем "длинные" списки для подсчета.
            # Отрезок кода проверяет на книги и фотопечать и формирует 1 список, но с разным наполнением
            for line in ex_list:
                # Проверка на копии. 2й уровень проверки - на фотопечать или развороты в книге
                dir_name = line[0].split('/')
                if re.fullmatch(r'\d+', dir_name[0]):
                    if re.search(r'\d+__\d+', dir_name[1]):
                        long_list.append(len(line) - 1)
                    elif re.search(r'cover', dir_name[1]):
                        long_list.append(1)
                elif re.search(r'\d+-\d+_pcs', dir_name[0]):
                    copy_value = re.split(r'[-_]', dir_name[0])[1]
                    if re.search(r'\d+__\d+', dir_name[1]):
                        pages_count = len(line) - 1
                        count = 1
                        while count <= int(copy_value):
                            long_list.append(pages_count)
                            count += 1
                    elif re.search(r'cover', dir_name[1]):
                        count = 1
                        while count <= int(copy_value):
                            long_list.append(1)
                            count += 1
            # Измеряем "длинные" списки и формируем из них читаемую информацию. Метод возвращает список из
            # элементов в порядке: счетчик обложек, счетчик разворотов, комплексный счетчик
            cover_count = len(long_list)
            page_count = sum(long_list)
            complex_count = []
            min_value = min(long_list)
            max_value = max(long_list)
            while min_value <= max_value:
                item_value = long_list.count(min_value)
                if item_value:
                    unit_ex = f"{item_value}/{min_value}"
                    complex_count.append(unit_ex)
                min_value += 1
            complex_count = " ".join(complex_count)
            return [cover_count, page_count, complex_count]

        def elem_check(constant, pic_count):
            # Метод анализирует значения счетчика и сравнивает их с значениями в папке констант.
            # Если количество разворотов по экземплярамм = количеству разворотов в константах -> Внутрянки одинаковые
            # Если в константах есть обложка -> обложки одинаковые
            # Если совпали 2 предыдущих условия -> это копии
            # В остальных случаях - индивидуально
            # Еckи в книге 1 элемент - возвращается значение None

            elem_type = "Индивидуально"
            if constant:
                const_page_count = 0
                cover_exist = None
                for i in constant:
                    if not re.search(r'cover', i):
                        splited = re.split(r'_', i)
                        const_page_count += int(splited[1])
                    elif re.search(r'cover', i):
                        cover_exist = True
                if pic_count[1] == const_page_count and cover_exist and pic_count[0] == 1:
                    elem_type = None
                elif pic_count[1] == const_page_count and cover_exist:
                    elem_type = "Копии"
                elif pic_count[1] == const_page_count:
                    elem_type = "В_О"
                elif cover_exist:
                    elem_type = "О_О"
            return elem_type

        for name in ob_with_content:
            # Проверяем, что content был получен в предыдущем методе.
            if ob_with_content[name]['content'] is not None:
                path = ob_with_content[name]['path']
                for product in ob_with_content[name]['content']:
                    if product == 'PHOTO':
                        photo_calc_list = foto_count(f"{path}/{product}")
                        if photo_calc_list:
                            ob_with_content[name]['content'][product]['counts'] = photo_calc_list
                    else:
                        # Получаем списки из папок экземпляров и список папки Constant
                        exemplar_list = get_list.ex_list(f"{path}/{product}")
                        const_list = get_list.constant_list(f"{path}/{product}")
                        # Проверяем на то, что список экземпляров сформирован и считаем изображения внутри.
                        if exemplar_list:
                            count_info = count_fx(exemplar_list)
                            elem = elem_check(const_list, count_info)
                            count_info.append(elem)
                            ob_with_content[name]['content'][product]['counts'] = count_info
        return ob_with_content

    @staticmethod
    def __set_content_type(ob_with_count):
        """
        :param ob_with_count: Словарь из метода __content_count
        :return: Дополненый словарь. Перебираем содержимое заказов и прицепляем информацию из библиотеки продуктов:
        [0] - Тип - для обработчика и [1] - Название продукта (ссылка на библиотеку) для информации в стикере
        """

        # Загружаем библиотеку сохраненных продуктов
        book_lib = config.read_json_book_lib()

        # Перебирем ключи (заказы) в логе
        for order in ob_with_count:
            # Проверяем, что есть запись в ['content'] (заказ не пустой)
            if ob_with_count[order]['content']:
                # Перебираем содержимое заказа
                for content in ob_with_count[order]["content"]:
                    # Подход для всех продуктов: Пытаемся найти продукт быстро по совпадению типов.
                    # Если продукт не был найден быстрым способом, то перебираем весь словарь по-строчно.
                    # Быстрый способ
                    for product_type in book_lib:
                        check_value = False
                        if re.search(product_type, content):
                            for product_name in book_lib[product_type]:
                                if re.search(product_name, content):
                                    # Ключь ptype - список, который будет добвален в лог к продукту.
                                    ptype = {"type": [product_type, product_name]}
                                    ob_with_count[order]["content"][content].update(ptype)
                                    check_value = True
                                    break
                        if check_value:
                            break
                    # Медленный способ. Сработает, если категория не совпала.
                    else:
                        for product_type_again in book_lib:
                            check_value_again = False
                            for product_name_again in book_lib[product_type_again]:
                                if re.search(product_name_again, content):
                                    ptype_sec = {"type": [product_type_again, product_name_again]}
                                    ob_with_count[order]["content"][content].update(ptype_sec)
                                    check_value_again = True
                                    break
                            if check_value_again:
                                break
        return ob_with_count
