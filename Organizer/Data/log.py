import os
import re

import Data.config as config


class New_Log_Creator:
    @staticmethod
    def __check_file_log():
        """
        Проверка на существование лога файлов. Необходимо для работы скрипта. Если его нет, то создаем пустой файл для
        последующей записи.
        """
        if not os.path.isfile('Data/Settings/file_log.json'):
            config.write_json_log({})

    @staticmethod
    def __get_daydir_list() -> tuple:
        """
        :return: Метод возвращает список папок - дней, где элемент - абсолютный путь до папки.
        Возвращаются значения в обратном порядке.
        """
        # Получаем путь - папка куда сохраненяются заказы c сервера
        order_dir = config.read("working_dir", "order_main_dir")
        # Проверяем на то, что нужная нам строчка - папка и она соответствует названию, которое присваивает сервер.
        current_list = [f"{order_dir}/{day}" for day in os.listdir(order_dir) if re.fullmatch(r'202\d-\d\d-\d\d', day)]
        return tuple(current_list[::-1])

    @staticmethod
    def __get_order_list(path) -> tuple:
        """
        :param path: Передается путь "Папка сохранения заказов/День загрузки"
        :return: Возвращает список (кортеж) из папок - заказов отсортированный в обратном порядке.
        """
        # При формировании списка проверяем, что у заказа имя совпадает с автоматически формируемым.
        order_list = [name for name in os.listdir(path) if re.fullmatch(r'\d{6}', name)]
        return tuple(order_list[::-1])

    @staticmethod
    def __get_order_content(path) -> tuple:
        """
        Метод проверяет на то, что элемент - папка и она не находится в списке технических ограничений
        :param path: Путь до заказа
        :return: Метод возвращает кортеж. Значения - содержимое заказа
        """
        exclusions = ("_TO_PRINT", "TO_PRINT", "_ЕЩ_ЗКШТЕ")
        c_list = [name for name in os.listdir(path) if name not in exclusions and os.path.isdir(f'{path}/{name}')]
        return tuple(c_list)

    @staticmethod
    def __get_order_type(content, book_lib) -> list:
        """
        Подход для всех продуктов: Пытаемся найти продукт быстро по совпадению типов.
        Если продукт не был найден быстрым способом, то перебираем весь словарь по-строчно.
        :param content: Имена папок - продуктов.
        :param book_lib: Ссылка на библиотеку продуктов.
        :return: Возрващает список в виде (Категория продукта, Полное название продукта).
        Если продукт не определен - None.
        """
        # Быстрый способ
        if content != 'PHOTO':
            for product_type in book_lib:
                if re.search(product_type, content):
                    for product_name in book_lib[product_type]:
                        if re.match(product_name[::-1], content[::-1]):
                            return [product_type, product_name]
            # Долгий способ
            for product_type in book_lib:
                for product_name in book_lib[product_type]:
                    if re.match(product_name[::-1], content[::-1]):
                        return [product_type, product_name]

    @staticmethod
    def __get_order_count(path, name) -> list:
        def foto_count(c_path) -> list:
            """
            Метод для подсчета и типизации фотопечати Из загрузчика OB версии 2,0,0,4.
            :param c_path: Принимается путь, где расположены фотографии.
            :return: Возвращается список словарей в виде [{Бумага и формат: количество}, ...]
            """
            foto_format_and_count_list = []
            for foto_paper in os.listdir(f"{c_path}/_ALL/Фотопечать"):
                # Перебираем папки (бумага) и назначаем тип.
                match foto_paper:
                    case "Глянцевая":
                        paper_type = 'Fuji GL'
                    case "Матовая":
                        paper_type = 'Fuji MT'
                    case "Silk":
                        paper_type = "Fuji Silk"
                    case _:
                        paper_type = "Fuji ???"
                foto_unit_dict = {}
                for foto_format in os.listdir(f"{c_path}/_ALL/Фотопечать/{foto_paper}"):
                    # Перебираем форматы и получаем формат в виде (10х15) и мультипликатор, 
                    # который влияет на количество фото внутри папки.
                    f_name, f_format, multiplier = re.split(r" |--", foto_format)
                    # Подсчитываются фото внутри папки
                    f_count = len(os.listdir(f"{c_path}/_ALL/Фотопечать/{foto_paper}/{foto_format}"))
                    name_to_add = f"{paper_type} {f_format}"
                    value_to_add = int(multiplier) * f_count
                    # Формируем словарь. 
                    # Если изображение есть, значения обновляются, если его нет - значение добавляется.
                    if name_to_add in foto_unit_dict:
                        foto_unit_dict[name_to_add] += value_to_add
                    else:
                        foto_unit_dict.update({name_to_add: value_to_add})
                foto_format_and_count_list.append(foto_unit_dict)
            if foto_format_and_count_list:
                return foto_format_and_count_list

        def pic_check(pic) -> bool:
            """
            Метод проверки изображений на совпадение паттернам, которые присваиваются программой OB.
            :param pic: Принимаем имя изображения.
            :return: Возвращаем булевое значение Тру или Фолс, в зависимости от результата работы метода.
            """
            patterns = (r'\d+__\d+\.jpg', r'cover_\d+\.jpg',  # Паттерны для обычных изображений
                        r'\d+__\d+-\d+_pcs\.jpg', r'cover_\d+-\d+_pcs\.jpg',  # Патерны для изображений - копий
                        r'\d+_\d+_pcs\.jpg', r'cover_\d+_pcs\.jpg')  # Паттерны изображений из констант
            for p in patterns:
                if re.fullmatch(p, pic):
                    return True
            return False

        def get_complex_count(ex_list) -> str:
            """
            Метод для формирования комплексного счетчика для книг в тираже.
            :param ex_list: Принимаем "длинный" список, где элемент - количество разворотов в экземпляре.
            :return: Возвращается строка в виде 2/4 3/5 и тд.
            """
            complex_count = []
            min_value = min(ex_list)
            max_value = max(ex_list)
            while min_value <= max_value:
                item_value = ex_list.count(min_value)
                if item_value:
                    unit_ex = f"{item_value}/{min_value}"
                    complex_count.append(unit_ex)
                min_value += 1
            complex_count = " ".join(complex_count)
            return complex_count

        def get_combination(cover_count, page_count, const_list) -> str:
            """
            Метод для определения совмещения книг в тираже.
            :param cover_count: Общее количество обложек в тираже.
            :param page_count: Общее количество разворотов в тираже
            :param const_list: Список изображений из папки Constant
            :return: Строку, если было определено совмещение. None для 1 книги
            """
            # Еcли в книге 1 элемент - возвращается значение None
            if cover_count > 1:
                if const_list:
                    cover_exist = False
                    const_page_count = 0
                    for const_name in const_list:
                        if re.fullmatch(r'cover_\d+_pcs\.jpg', const_name):
                            cover_exist = True
                        if re.fullmatch(r'\d\d\d_\d+_pcs\.jpg', const_name):
                            splited = re.split(r'_', const_name)
                            const_page_count += int(splited[1])
                    # Если совпали 2 следующих условия -> это копии
                    if cover_exist and const_page_count == page_count:
                        return "Копии"
                    # Если в константах есть обложка -> обложки одинаковые
                    elif cover_exist:
                        return 'О_О'
                    # Если количество разворотов по экземплярамм = количеству в константах -> Внутрянки одинаковые
                    elif const_page_count == page_count:
                        return 'В_О'
                    # В остальных случаях -> индивидуально
                return 'Индивидуально'

        def book_count(c_path) -> list:
            """
            Основной метод подсчета и определения совмещения для тиражей книг
            :param c_path: Принимается путь до тиража
            :return: Возвращается список в формате 
            [Общее кол-во обложек, общее кол-во разворотов, комплексный счетчик, порядок совмещения обложек и блоков],
            """
            ex_list = []
            const_list = []
            for dirs in os.listdir(c_path):
                c_dir = f"{c_path}\\{dirs}"
                # проверяем, что имя экземпяра совпадает с програмным и он в одиночном количестве
                if re.fullmatch(r'\d\d\d', dirs):
                    pic_list = [pic for pic in os.listdir(c_dir) if pic_check(pic)]
                    pic_count = len(pic_list) - 1
                    ex_list.append(1 if pic_count == 0 else pic_count)
                # Проверка для экземпляров - копий 
                elif re.fullmatch(r'\d\d\d-\d+_pcs', dirs):
                    pic_pcs_list = [pic for pic in os.listdir(c_dir) if pic_check(pic)]
                    pic_pcs_count = len(pic_pcs_list) - 1
                    multiplier = int(re.split('[-_]', dirs)[1])
                    ex_list.extend([1] * multiplier if pic_pcs_count == 0 else [pic_pcs_count] * multiplier)
                # Для папки констант
                elif re.fullmatch(r'Constant', dirs):
                    pic_const_list = [pic for pic in os.listdir(c_dir) if pic_check(pic)]
                    const_list.extend(pic_const_list)
            # Отправляем список в дочерние методы для обработки 
            if ex_list:
                cover_count = len(ex_list)
                page_count = sum(ex_list)
                complex_count = get_complex_count(ex_list)
                combination = get_combination(cover_count, page_count, const_list)
                return [cover_count, page_count, complex_count, combination]

        # Основная часть метода __get_order_count. Возвращает списки в зависимости от того, книга это, или фотопечать.
        content_path = f'{path}/{name}'
        if name == 'PHOTO':
            return foto_count(content_path)
        else:
            return book_count(content_path)

    def __content_processing(self, path, content, book_lib) -> dict:
        """
        Обработка заказа. Подсчет файлов и определение типа заказа
        :param path: Путь до заказа
        :param content: Список содержимого для заказа
        :param book_lib: Ссылка на библиотеку продуктов для сравнения.
        :return: Возвращается словарь с содержимым заказа. Всегда должны быть записаны 'counts' и 'type' и их значения.
        Если их не удалось определить, то записывается None
        """
        content_dict = {}
        for name in content:
            order_count = self.__get_order_count(path, name)
            order_type = self.__get_order_type(name, book_lib)
            product_dict = {name: {
                'counts': order_count,
                'type': order_type
            }}
            content_dict.update(product_dict)
        return content_dict

    def __get_order_dict(self, day, name, book_lib) -> dict:
        """ Если содержимое заказа пустое, то метод ничего не возвращает.
        :param day: Абсолютный путь до папки c днем, куда загрузился заказ.
        :param name: Имя заказа.
        :param book_lib: Ссылка на библиотеку продуктов для определения типа книги.
        :return:  Метод возвращает полностью сформированный словарь для заказа, путь которого передан в параметре path.
        """
        # Определяем постоянные записи к словарю заказа
        creation_date = day.split('/')[-1]
        path = f'{day}/{name}'
        # Получаем содержимое заказа и отправляем это на на обработку. Получаем словарь к каждому значению.
        content = self.__get_order_content(path)
        if content:
            product_dict = self.__content_processing(path, content, book_lib)
            order_dict = {name: {
                'creation_date': creation_date,
                'path': path,
                'content': product_dict
            }}
            return order_dict

    def main(self):
        """
        Основной метод для формирования лога.
        """
        self.__check_file_log()  # Вызываем проверку на существование лога.
        # Получаем существующий лог и библиотеку для сравнения
        file_log = config.read_json_orders_log()
        book_lib = config.read_json_book_lib()
        check_depth = int(config.read('logs', 'check_deep'))  # Глубина проверки
        run_flag = True  # Флаг для остановки функции
        # Получаем список дней для анализа
        daydir_list = self.__get_daydir_list()
        for day in daydir_list:
            if not run_flag:
                break
            # Получаем список заказов в дне.
            order_list = self.__get_order_list(day)
            if order_list:
                for name in order_list:
                    # Формируем словарь для продукта
                    order_dict = self.__get_order_dict(day, name, book_lib)
                    if order_dict:
                        # Когда глубина проверки = 0 - останавливаем цикл и пишем лог в файл.
                        # Если записать -1, проверка осуществлятся не будет и перезапишутся все заказы.
                        if check_depth == 0:
                            run_flag = False
                            break
                        # Если такого заказа нет в текущем логе - обновляем его
                        if name not in file_log:
                            file_log.update(order_dict)
                        # Если заказ есть в логе, но их содержимое не совпадает - обновляем
                        elif name in file_log and file_log[name] != order_dict[name]:
                            file_log.update(order_dict)
                        # Если заказ есть в логе и их словари совпадают, то, на всякий случай, обнавляем лог.
                        # Уменьшаем значение глубины проверки.
                        elif name in file_log and file_log[name] == order_dict[name]:
                            check_depth -= 1
                            file_log.update(order_dict)
        config.write_json_log(file_log)
