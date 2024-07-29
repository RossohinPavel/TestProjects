import os
import re

from Data.Legacy.decorators import time_and_size
import Data.config as config


class New_Log_Creator:
    @staticmethod
    def __check_file_log():
        """
        Проверяем на существование лога файлов. Необходимо для работы скрипта. Если его нет, то создаем пустой файл для
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
        :param path:
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
        :param content: Имена папок - продуктов
        :param book_lib: Ссылка на библиотеку продуктов
        :return: Возрващает кортеж в виде (Категория продукта, Полное название продукта).
        Если продукт не определен - None
        """
        # Быстрый способ
        if content != 'PHOTO':
            for product_type in book_lib:
                if re.search(product_type, content):
                    for product_name in book_lib[product_type]:
                        if re.search(product_name, content):
                            return [product_type, product_name]

    @staticmethod
    def __get_order_count(path, name) -> list:
        def foto_count(c_path) -> list:
            # Метод для подсчета и типизации фотопечати Из загрузчика OB версии 2,0,0,4
            foto_format_and_count_list = []
            for foto_paper in os.listdir(f"{c_path}/_ALL/Фотопечать"):
                match foto_paper:
                    case "Глянцевая": paper_type = 'Fuji GL'
                    case "Матовая": paper_type = 'Fuji MT'
                    case "Silk": paper_type = "Fuji Silk"
                    case _: paper_type = "Fuji ???"
                foto_unit_dict = {}
                for foto_format in os.listdir(f"{c_path}/_ALL/Фотопечать/{foto_paper}"):
                    f_name, f_format, multiplier = re.split(r" |--", foto_format)
                    f_count = len(os.listdir(f"{c_path}/_ALL/Фотопечать/{foto_paper}/{foto_format}"))
                    name_to_add = f"{paper_type} {f_format}"
                    value_to_add = int(multiplier) * f_count
                    if name_to_add in foto_unit_dict:
                        foto_unit_dict[name_to_add] += value_to_add
                    else:
                        foto_unit_dict.update({name_to_add: value_to_add})
                foto_format_and_count_list.append(foto_unit_dict)
            if foto_format_and_count_list:
                return foto_format_and_count_list

        def get_file_list(c_path) -> list:
            file_list = []
            for roots, dirs, files in os.walk(c_path):
                for file in files:
                    abs_path = os.path.join(roots, file)
                    rel_path = os.path.relpath(abs_path, c_path)
                    file_list.append(rel_path)
            if file_list:
                return file_list

        def pic_check(file_list) -> tuple:
            long_list = []
            const_list = []
            ex = 0
            const_ex = []
            for line in file_list:
                splitted = line.split('\\')
                if len(splitted) == 2 and splitted[0] not in ('Covers', 'Variable'):
                    index = file_list.index(line)
                    prev_splited = file_list[index - 1].split("\\")
                    if splitted[0] != prev_splited[0]:
                        if ex:
                            long_list.append(ex)
                        if const_ex:
                            long_list.extend(const_ex)
                        ex = 0
                        const_ex = []
                    if re.fullmatch(r'\d\d\d', splitted[0]) and not re.search('cover', splitted[1]):
                        ex += 1
                    elif re.fullmatch(r'\d\d\d-\d+_pcs', splitted[0]) and not re.search('cover', splitted[1]):
                        multiplier = int(re.split('[-_]', splitted[0])[1])
                        for i in range(multiplier):
                            if len(const_ex) == multiplier:
                                const_ex[i] += 1
                            else:
                                const_ex.insert(i, 1)
                    elif re.fullmatch(r'Constant', splitted[0]):
                        const_list.append(splitted[1])
            return long_list, const_list

        def get_complex_count(ex_list) -> str:
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
            # Метод анализирует значения счетчика и сравнивает их с значениями в папке констант.
            # Если количество разворотов по экземплярамм = количеству разворотов в константах -> Внутрянки одинаковые
            # Если в константах есть обложка -> обложки одинаковые
            # Если совпали 2 предыдущих условия -> это копии
            # В остальных случаях - индивидуально
            # Еcли в книге 1 элемент - возвращается значение None
            if const_list and cover_count > 1:
                cover_exist = False
                const_page_count = 0
                for const_name in const_list:
                    if re.fullmatch(r'cover_\d+_pcs\.jpg', const_name):
                        cover_exist = True
                    if re.fullmatch(r'\d\d\d_\d+_pcs\.jpg', const_name):
                        splited = re.split(r'_', const_name)
                        const_page_count += int(splited[1])
                if cover_exist and const_page_count == page_count:
                    return "Копии"
                elif cover_exist:
                    return 'О_О'
                elif const_page_count == page_count:
                    return 'В_О'
                else:
                    return 'Индивидуально'

        def book_count(c_path) -> list:
            file_list = get_file_list(c_path)
            if file_list:
                ex_list, const_list = pic_check(file_list)
                if ex_list:
                    cover_count = len(ex_list)
                    page_count = sum(ex_list)
                    complex_count = get_complex_count(ex_list)
                    combination = get_combination(cover_count, page_count, const_list)
                    return [cover_count, page_count, complex_count, combination]

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

    @time_and_size
    def main(self):
        self.__check_file_log()  # Вызываем проверку на существование лога.
        file_log = config.read_json_orders_log()
        book_lib = config.read_json_book_lib()
        check_depth = 9  # Глубина проверки
        run_flag = True  # Флаг для остановки функции
        daydir_list = self.__get_daydir_list()
        for day in daydir_list:
            if not run_flag:
                break
            order_list = self.__get_order_list(day)
            if order_list:
                for name in order_list:
                    order_dict = self.__get_order_dict(day, name, book_lib)
                    if order_dict:
                        if name not in file_log:
                            file_log.update(order_dict)
                        elif name in file_log and file_log[name] != order_dict[name]:
                            file_log.update(order_dict)
                        elif name in file_log and file_log[name] == order_dict[name]:
                            check_depth -= 1
                            file_log.update(order_dict)
                    if check_depth == 0:
                        run_flag = False
                        break
        config.write_json_log(file_log)


New_Log_Creator().main()
