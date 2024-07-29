import tkinter as tk
from tkinter.ttk import Combobox


import Data.windows as windows
import Data.config as config
import Data.get_graphics as get_grap


class Get_sticker(windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Генерация наклейки")
        self.child_root.geometry("300x240")
        self.to_parent_center(root)
        self.order_name = tk.StringVar()  # Переменная для сохранения введеного номера заказа.
        self.stic_entry_var = tk.StringVar()  # Переменная для вывода информации по заказу
        self.__show_widgets()

    def __show_widgets(self):
        ask_order_lbl = tk.Label(self.child_root, text="Введите номер заказа")
        ask_order_lbl.place(x=50, y=2)
        order_name_entry = tk.Entry(self.child_root, textvariable=self.order_name)
        order_name_entry.place(x=50, y=22)
        order_name_entry.focus_set()
        order_name_entry.bind('<Return>', self.get_stic)
        get_order_inf_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                      text='Получить', command=self.get_stic)
        get_order_inf_btn.place(x=180, y=10)
        # Лейбл для вывода информации о заказе
        stic_inf_lbl = tk.Label(self.child_root, textvariable=self.stic_entry_var, justify=tk.LEFT)
        stic_inf_lbl.place(x=0, y=40)
        to_clip_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                text="Скопировать в буфер", command=self.to_clip_board)
        to_clip_btn.place(x=2, y=210)
        exit_btn = tk.Button(self.child_root, text="Закрыть", relief=tk.FLAT, fg="#eee", bg="#454545",
                             command=self.child_root.destroy)
        exit_btn.place(x=240, y=210)
        self.child_root.grab_set()
        self.child_root.wait_window()

    def get_stic(self, event=None):
        # Метод - событие для получения номера заказа из поля ввода.
        order_name = self.order_name.get()
        order_log = config.read_json_orders_log()
        # Проверяем, что заказ есть в логе и он не пустой (как минимум созданы папки с именами тиражей)
        if order_name in order_log:
            content = order_log[order_name]['content']
            stic_inf_list = self.forming_line(content)
            self.stic_entry_var.set(self.clear_stic_list(stic_inf_list))
            self.to_clip_board()
            self.order_name.set("")
        else:
            self.order_name.set("")

    @staticmethod
    def forming_line(content) -> list:
        stic_list = []  # Список для хранения информации об основных продуктах
        stic_list_sub = []  # Вспомогательный список для субпродуктов (Очищается от повторений)
        book_lib = config.read_json_book_lib()
        for name in content:
            if content[name] and name != "PHOTO":  # Проверяем, что заказ не пустой.
                # Проверяем на счетчики и на определение типа.
                if content[name]['counts'] and content[name]['type']:
                    counts = content[name]['counts']
                    ptype = content[name]['type']
                    pdict = book_lib[ptype[0]][ptype[1]]
                    comb = f" -- {counts[3]}" if counts[3] else ""
                    match ptype[0]:
                        case "Фотокнига Стандарт" | "Фотокнига ЛЮКС" | "Фотокнига Классик" | "Фотопланшет Стандарт" | "Layflat":
                            if pdict['short_name'] in ("пМикс", "кМикс"):
                                stic_list.append(
                                    f"{pdict['short_name']} {counts[2]} {pdict['book_option']} {pdict['lamination']}{comb}")
                            else:
                                stic_list.append(
                                    f"{pdict['short_name']} {pdict['book_format']} {counts[2]} {pdict['book_option']} {pdict['lamination']}{comb}")
                        case "Фотоальбом полиграфический" | "Фотоальбом PUR" | "Фотокнига Flex Bind":
                            stic_list.append(
                                f"{pdict['short_name']} {pdict['book_format']} {counts[2]} {pdict['lamination']}{comb}")
                        case "Фотожурнал":
                            stic_list.append(f"{pdict['short_name']} {pdict['book_format']} {counts[2]}{comb}")
                        case "Фотопапка":
                            stic_list.append(
                                f"{pdict['short_name']} {counts[2].split('/')[0]}шт {pdict['lamination']}{comb}")
                        case "Фотопечать SRA" | "Фотопечать" | "Субпродукты":
                            stic_list_sub.append(f"{pdict['short_name']}")
                # Когда тип не определен, то добавляем полное имя тиража в список, вместо комплексной информации.
                elif content[name]['counts'] and content[name]['type'] is None:
                    stic_list.append(name)
            elif name == "PHOTO":
                stic_list_sub.append("+фото")
        # Очищаем вспомогательный список от дубликатов
        clear_sub_list = list(set(stic_list_sub))
        if clear_sub_list:
            for i in clear_sub_list:
                stic_list.append(i)
        return stic_list

    @staticmethod
    def clear_stic_list(st_list) -> str:
        stic = '\n'.join(st_list)
        return stic

    def to_clip_board(self):
        to_clip = self.stic_entry_var.get()
        if to_clip:
            self.child_root.clipboard_clear()
            self.child_root.clipboard_append(to_clip)


class get_calc_info:
    def __init__(self, order_content, book_lib):
        self.content = order_content
        self.book_lib = book_lib

    def __calc_fotobook_standart(self, product_class, product_name, cover_count, page_count):
        # Проверяем на вхождение этого класса и продукта в библиотеку и получаем его значения
        if product_class in self.book_lib and product_name in self.book_lib[product_class]:
            product_lib = self.book_lib[product_class][product_name]
            cover_mat_dict = {product_lib['cover_material']: cover_count}
            cover_carton_dict = {product_lib['cover_carton']: int(cover_count) * 2}
            page_mat_dict = {product_lib['page_material']: page_count}
            page_carton_count = 0
            if product_lib['book_option'] == 'б/у':
                page_carton_count = 2 * int(cover_count)
            elif product_lib['book_option'] == 'с/у':
                page_carton_count = int(page_count) + int(cover_count)
            elif product_lib['book_option'] == "с/у1.2":
                page_carton_count = int(page_count) * 2
            page_carton_dict = {product_lib['book_format']: page_carton_count}
            return cover_carton_dict, page_carton_dict, cover_mat_dict, page_mat_dict

    def __calc_flex_bind(self, product_class, product_name, cover_count, page_count):
        if product_class in self.book_lib and product_name in self.book_lib[product_class]:
            product_lib = self.book_lib[product_class][product_name]
            book_format = product_lib["book_format"]
            cover_mat_dict = {product_lib['cover_material']: cover_count}
            cover_carton_dict = {product_lib['cover_carton']: int(cover_count) * 2}
            page_mat_dict = {}
            if book_format in ("20x20", "30x20г"):
                # Количество полезных отпечатков + 2 белые листы (за каждую обложку)
                true_page_count = (cover_count * 2) + (page_count * 2)
                # Вычитаем из этого количества отпечатки для первого листа
                true_page_count = true_page_count - (6 * cover_count)
                flex_count = int(true_page_count / 4) + 3
                page_mat_dict = {product_lib["page_material"]: flex_count}
            else:
                true_page_count = (page_count + 1) * cover_count
                page_mat_dict = {product_lib["page_material"]: true_page_count}
            return cover_carton_dict, {}, cover_mat_dict, page_mat_dict

    def __calc_poli_alb(self, product_class, product_name, cover_count, page_count):
        # Проверяем на вхождение этого класса и продукта в библиотеку и получаем его значения
        if product_class in self.book_lib and product_name in self.book_lib[product_class]:
            product_lib = self.book_lib[product_class][product_name]
            cover_mat_dict = {product_lib['cover_material']: cover_count}
            cover_carton_dict = {product_lib['cover_carton']: int(cover_count) * 2}
            page_mat_dict = {product_lib['page_material']: page_count + cover_count}
            return cover_carton_dict, {}, cover_mat_dict, page_mat_dict

    def __calc_poli_jur(self, product_class, product_name, cover_count, page_count):
        # Проверяем на вхождение этого класса и продукта в библиотеку и получаем его значения
        if product_class in self.book_lib and product_name in self.book_lib[product_class]:
            product_lib = self.book_lib[product_class][product_name]
            cover_mat_dict = {product_lib['cover_material']: cover_count}
            page_mat_dict = {product_lib['page_material']: int((page_count - cover_count) / 2)}
            return {}, {}, cover_mat_dict, page_mat_dict

    def __calc_foto_pap(self, product_class, product_name, cover_count, page_count):
        # Проверяем на вхождение этого класса и продукта в библиотеку и получаем его значения
        if product_class in self.book_lib and product_name in self.book_lib[product_class]:
            product_lib = self.book_lib[product_class][product_name]
            product_short_name = product_lib["short_name"]
            cover_mat_dict = {product_lib['cover_material']: cover_count}
            page_mat_dict = {product_lib['page_material']: page_count}
            cover_carton_dict = ""
            if product_short_name != "Трио":
                cover_carton_dict = {product_lib['cover_carton']: cover_count * 2}
            else:
                cover_carton_dict = {product_lib['cover_carton']: cover_count * 3}
            return cover_carton_dict, {}, cover_mat_dict, page_mat_dict

    def main(self) -> dict:
        # Пробегаемся по словарю заказа и проверяем, что сформирован счетчик и определен тип
        mat_dict = {"Переплетный картон": [], "Межстраничный картон": [],
                    "Материал для фотопечати": [], "Материал для печати книг": []}
        content = self.content
        for name in content:
            if content[name]['counts'] and content[name]['type']:
                product_class = content[name]['type'][0]
                product_name = content[name]['type'][1]
                cover_count = content[name]['counts'][0]
                page_count = content[name]['counts'][1]
                match product_class:
                    case "Фотокнига Стандарт" | "Фотокнига ЛЮКС" | "Фотокнига Классик" | "Фотопланшет Стандарт" | "Layflat":
                        product_info = self.__calc_fotobook_standart(
                            product_class, product_name, cover_count, page_count)
                        if product_info:
                            mat_dict["Переплетный картон"].append(product_info[0])
                            mat_dict["Межстраничный картон"].append(product_info[1])
                            mat_dict["Материал для печати книг"].append(product_info[2])
                            mat_dict["Материал для печати книг"].append(product_info[3])
                    case "Фотокнига Flex Bind":
                        product_info = self.__calc_flex_bind(product_class, product_name, cover_count, page_count)
                        if product_info:
                            mat_dict["Переплетный картон"].append(product_info[0])
                            mat_dict["Межстраничный картон"].append(product_info[1])
                            mat_dict["Материал для печати книг"].append(product_info[2])
                            mat_dict["Материал для печати книг"].append(product_info[3])
                    case "Фотоальбом полиграфический" | "Фотоальбом PUR":
                        product_info = self.__calc_poli_alb(product_class, product_name, cover_count, page_count)
                        if product_info:
                            mat_dict["Переплетный картон"].append(product_info[0])
                            mat_dict["Межстраничный картон"].append(product_info[1])
                            mat_dict["Материал для печати книг"].append(product_info[2])
                            mat_dict["Материал для печати книг"].append(product_info[3])
                    case "Фотожурнал":
                        product_info = self.__calc_poli_jur(product_class, product_name, cover_count, page_count)
                        if product_info:
                            mat_dict["Переплетный картон"].append(product_info[0])
                            mat_dict["Межстраничный картон"].append(product_info[1])
                            mat_dict["Материал для печати книг"].append(product_info[2])
                            mat_dict["Материал для печати книг"].append(product_info[3])
                    case "Фотопапка":
                        product_info = self.__calc_foto_pap(product_class, product_name, cover_count, page_count)
                        if product_info:
                            mat_dict["Переплетный картон"].append(product_info[0])
                            mat_dict["Межстраничный картон"].append(product_info[1])
                            mat_dict["Материал для печати книг"].append(product_info[2])
                            mat_dict["Материал для печати книг"].append(product_info[3])
            elif name == 'PHOTO' and content[name]['counts']:
                cover_count = content[name]['counts']
                mat_dict["Материал для фотопечати"].extend(cover_count)
        # Объединяем похожие элемнты в строчках словаря и сортируем их по убыванию
        for mat_type in mat_dict:
            if mat_dict[mat_type]:
                # Объединяем элементы в словаре
                merge_dict = {}
                for name_dict in mat_dict[mat_type]:
                    for name in name_dict:
                        if name not in merge_dict:
                            merge_dict.update({name: name_dict[name]})
                        elif name in merge_dict:
                            merge_dict[name] += name_dict[name]
                # Сортируем по убыванию значений
                sorted_dict = {}
                sorted_keys = sorted(merge_dict, key=merge_dict.get, reverse=True)
                for name in sorted_keys:
                    sorted_dict.update({name: merge_dict[name]})
                mat_dict[mat_type] = sorted_dict
        return mat_dict


class get_order_material(windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Расчет расодного материала для заказа")
        self.child_root.geometry("400x350")
        self.to_parent_center(root)
        self.order_name = tk.StringVar()  # Переменная для сохранения введеного номера заказа.
        self.product_name = tk.StringVar()  # Переменная для сохранения имен продуктов.
        self.mat_entry_var = tk.StringVar()  # Переменная для вывода информации картону и межстраничке
        self.print_entry_var = tk.StringVar()  # Переменная для вывода информации по печатным матералам
        self.__show_widgets()

    def __show_widgets(self):
        ask_order_lbl = tk.Label(self.child_root, text="Введите номер заказа")
        ask_order_lbl.place(x=110, y=2)
        order_name_entry = tk.Entry(self.child_root, textvariable=self.order_name)
        order_name_entry.place(x=110, y=22)
        order_name_entry.focus_set()
        order_name_entry.bind('<Return>', self.get_order_mat)
        get_order_inf_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                      text='Посчитать', command=self.get_order_mat)
        get_order_inf_btn.place(x=250, y=10)
        # Лейбл для вывода информации о заказе
        self.order_name_lbl = tk.Label(self.child_root)
        self.order_name_lbl.place(x=60, y=44)
        order_canvas = tk.Canvas(self.child_root, bg='black', height=1, width=400)
        order_canvas.place(x=0, y=62)
        inf_frame = tk.Frame(self.child_root, width=400, height=250)
        inf_frame.place(x=0, y=66)
        product_name_lbl = tk.Label(inf_frame, textvariable=self.product_name, justify=tk.LEFT)
        product_name_lbl.grid(row=0, column=0, columnspan=3, sticky=tk.NW)
        mat_inf_lbl_left = tk.Label(inf_frame, textvariable=self.mat_entry_var, justify=tk.LEFT)
        mat_inf_lbl_left.grid(row=1, column=0, sticky=tk.NW)
        print_inf_lbl_right = tk.Label(inf_frame, textvariable=self.print_entry_var, justify=tk.LEFT)
        print_inf_lbl_right.grid(row=1, column=1, sticky=tk.NW)
        to_clip_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                text="Скопировать в буфер")
        to_clip_btn.place(x=2, y=320)
        exit_btn = tk.Button(self.child_root, text="Закрыть", relief=tk.FLAT, fg="#eee", bg="#454545",
                             command=self.child_root.destroy)
        exit_btn.place(x=340, y=320)
        self.child_root.grab_set()
        self.child_root.wait_window()

    @staticmethod
    def get_product_name_and_complex_count(name) -> str:
        order_content_log = config.read_json_orders_log()[name]['content']
        product_name_list = []
        check_list = ["Фотокнига Стандарт", "Фотокнига ЛЮКС", "Фотокнига Flex Bind", "Фотокнига Классик",
                      "Фотопланшет Стандарт", "Layflat", "Фотоальбом полиграфический", "Фотоальбом PUR",
                      "Фотожурнал", "Фотопапка"]
        for name in order_content_log:
            if order_content_log[name]['type'] and order_content_log[name]['counts']:
                product_type = order_content_log[name]['type'][0]
                if product_type in check_list:
                    product_name = order_content_log[name]['type'][1]
                    counts = order_content_log[name]['counts'][2]
                    product_name_list.append(f"{product_name} -- {counts}")
        for name in order_content_log:
            if name == "PHOTO" and order_content_log[name]['counts']:
                photo_dict = order_content_log[name]['counts']
                photo_list = []
                for line in photo_dict:
                    for name in line:
                        photo_list.append(f"{name} -- {line[name]}")
                product_name_list.extend(photo_list)
        return "\n".join(product_name_list)

    def get_order_mat(self, event=None):
        # Метод - событие для получения номера заказа из поля ввода.
        order_name = self.order_name.get()
        order_log = config.read_json_orders_log()
        # Проверяем, что заказ есть в логе и он не пустой (как минимум созданы папки с именами тиражей)
        if order_name in order_log and order_log[order_name]['content']:
            # Получим библиотеку заранее 1 раз. Чтобы не обращаться в цилке к ней по несколько раз
            # Передаем содержимое заказа и библиотеку
            calc_info = get_calc_info(order_log[order_name]['content'], config.read_json_book_lib())
            self.show_calc_info(calc_info.main())
            self.product_name.set(self.get_product_name_and_complex_count(order_name))
            self.order_name_lbl.config(text=f"Расчет расходных материалов для заказа: {order_name}")
            self.order_name.set("")
        else:
            self.order_name.set("")

    def show_calc_info(self, calc_info):
        merge_str_carton = ""
        merge_str_print_mat = ""
        # Объединяем словари и списки для вывода информации
        for mat_type in calc_info:
            # Проверяем на пустые значения
            if calc_info[mat_type]:
                if mat_type != "Материал для печати книг":
                    mat_list = []
                    for mat_dict in calc_info[mat_type]:
                        mat_list.append(f"{mat_dict} - {calc_info[mat_type][mat_dict]} шт")
                    mat_str = "\n    ".join(mat_list)
                    merge_str_carton += f"{mat_type}:\n    {mat_str}\n"
                else:
                    mat_list = []
                    for mat_dict in calc_info[mat_type]:
                        mat_list.append(f"{mat_dict} - {calc_info[mat_type][mat_dict]} шт")
                    mat_str = "\n    ".join(mat_list)
                    merge_str_print_mat += f"{mat_type}:\n    {mat_str}\n"
        self.mat_entry_var.set(merge_str_carton.rstrip('\n'))
        self.print_entry_var.set(merge_str_print_mat.rstrip('\n'))


class get_period_material(windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Расчет расходного материала для периода")
        self.child_root.geometry("600x500")
        self.to_parent_center(root)
        self.order_name = tk.StringVar()  # Переменная для сохранения введеного номера заказа.
        self.mat_entry_var = tk.StringVar()  # Переменная для вывода информации картону и межстраничке
        self.photo_print_val = tk.StringVar()   # Переменная для вывода информаци по фотопечати
        self.book_print_val = tk.StringVar()  # Переменная для вывода информации по печатным матералам
        self.__show_widgets()

    def __show_widgets(self):
        ask_order_lbl = tk.Label(self.child_root, text="Укажите период для подсчета")
        ask_order_lbl.place(x=6, y=2)
        start_date_lbl = tk.Label(self.child_root, text='C:')
        start_date_lbl.place(x=12, y=25)
        self.start_date_combo = Combobox(self.child_root, values=self.__get_date_period(), state="readonly")
        self.start_date_combo.place(x=30, y=24)
        end_date_lbl = tk.Label(self.child_root, text="По:")
        end_date_lbl.place(x=5, y=51)
        self.end_date_combo = Combobox(self.child_root, values=self.__get_date_period(), state="readonly")
        self.end_date_combo.place(x=30, y=50)
        get_order_inf_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                      text='Посчитать', command=self.__main)
        get_order_inf_btn.place(x=180, y=30)
        separate_canvas = tk.Canvas(self.child_root, bg='black', height=1, width=600)
        separate_canvas.place(x=0, y=74)
        # Лейбл для вывода информации о заказе
        material_frame = tk.Frame(self.child_root, width=600, height=380)
        material_frame.place(x=0, y=80)
        mat_inf_lbl = tk.Label(material_frame, textvariable=self.mat_entry_var, justify=tk.LEFT)
        mat_inf_lbl.grid(row=0, column=0, sticky=tk.NW)
        photo_print_inf_lbl = tk.Label(material_frame, textvariable=self.photo_print_val, justify=tk.LEFT)
        photo_print_inf_lbl.grid(row=0, column=1, sticky=tk.NW)
        book_print_inf_lbl = tk.Label(material_frame, textvariable=self.book_print_val, justify=tk.LEFT)
        book_print_inf_lbl.grid(row=0, column=2, sticky=tk.NW)
        to_clip_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545", state="disabled",
                                text="Скопировать в буфер")
        to_clip_btn.place(x=2, y=470)
        exit_btn = tk.Button(self.child_root, text="Закрыть", relief=tk.FLAT, fg="#eee", bg="#454545",
                             command=self.child_root.destroy)
        exit_btn.place(x=540, y=470)
        self.child_root.focus_set()
        self.child_root.grab_set()
        self.child_root.wait_window()

    @staticmethod
    def __get_date_period() -> list:
        # Получаем список дней доступных для подсчета периода. Сортируем по возрастанию (на всякий случай)
        log_lib = config.read_json_orders_log()
        period_list = []
        for name in log_lib:
            order_date = log_lib[name]['creation_date']
            if order_date not in period_list:
                period_list.append(order_date)
        return sorted(period_list)

    def __check_and_get_period_values(self):
        # Получаем значения и проверяем, что период указан в правильной последовательности. Елси нет - переворачиваем
        start_date = self.start_date_combo.get()
        end_date = self.end_date_combo.get()
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        return start_date, end_date

    @staticmethod
    def __merge_dict(dicts_to_merge):
        merge_dict = {}
        # Объединяем значения
        for line in dicts_to_merge:
            for name in line:
                if name in merge_dict:
                    merge_dict[name] += line[name]
                else:
                    merge_dict.update({name: line[name]})
        # Сортируем по убыванию значений
        sorted_dict = {}
        sorted_keys = sorted(merge_dict, key=merge_dict.get, reverse=True)
        for name in sorted_keys:
            sorted_dict.update({name: merge_dict[name]})
        return sorted_dict

    def show_calc_info(self, calc_info):
        merge_str_carton = ""
        merge_str_photo_mat = ""
        merge_str_book_mat = ""
        # Объединяем словари и списки для вывода информации
        for mat_type in calc_info:
            if mat_type in ('Переплетный картон', 'Межстраничный картон'):
                mat_list = []
                for mat_dict in calc_info[mat_type]:
                    mat_list.append(f"{mat_dict} - {calc_info[mat_type][mat_dict]} шт")
                mat_str = "\n    ".join(mat_list)
                merge_str_carton += f"{mat_type}:\n    {mat_str}\n"
            elif mat_type == 'Материал для фотопечати':
                mat_list = []
                for mat_dict in calc_info[mat_type]:
                    mat_list.append(f"{mat_dict} - {calc_info[mat_type][mat_dict]} шт")
                mat_str = "\n    ".join(mat_list)
                merge_str_photo_mat += f"{mat_type}:\n    {mat_str}\n"
            elif mat_type == 'Материал для печати книг':
                mat_list = []
                for mat_dict in calc_info[mat_type]:
                    mat_list.append(f"{mat_dict} - {calc_info[mat_type][mat_dict]} шт")
                mat_str = "\n    ".join(mat_list)
                merge_str_book_mat += f"{mat_type}:\n    {mat_str}\n"
        self.mat_entry_var.set(merge_str_carton.rstrip('\n'))
        self.photo_print_val.set(merge_str_photo_mat.rstrip('\n'))
        self.book_print_val.set(merge_str_book_mat.rstrip('\n'))

    def __main(self):
        # Получаем ограничивающие инструкции и запускаем счетчик.
        datas_tuple = self.__check_and_get_period_values()
        # Проверяем, что оба значения введены в комбобокс
        if datas_tuple[0] and datas_tuple[1]:
            start_date = datas_tuple[0]
            end_date = datas_tuple[1]
            order_log = config.read_json_orders_log()
            book_lib = config.read_json_book_lib()
            order_dict_lsit = []
            for name in order_log:
                # Проверяем на соответствие дат введеным ограничениям.
                # Получаем словари для заказов
                if start_date <= order_log[name]['creation_date'] <= end_date:
                    if order_log[name]['content']:
                        calc_info = get_calc_info(order_log[name]['content'], book_lib)
                        order_dict_lsit.append(calc_info.main())
            # Обрабатываем полученный список для совмещения значений
            cover_carton_list = []
            page_carton_list = []
            print_mat_list = []
            photo_print_mat_list = []
            for line in order_dict_lsit:
                if line['Переплетный картон']:
                    cover_carton_list.append(line['Переплетный картон'])
                if line['Межстраничный картон']:
                    page_carton_list.append(line['Межстраничный картон'])
                if line['Материал для печати книг']:
                    print_mat_list.append(line['Материал для печати книг'])
                if line['Материал для фотопечати']:
                    photo_print_mat_list.append(line['Материал для фотопечати'])
            cover_carton_list = self.__merge_dict(cover_carton_list)
            page_carton_list = self.__merge_dict(page_carton_list)
            print_mat_list = self.__merge_dict(print_mat_list)
            photo_print_mat_list = self.__merge_dict(photo_print_mat_list)
            complex_dict = {
                'Переплетный картон': cover_carton_list,
                'Межстраничный картон': page_carton_list,
                'Материал для фотопечати': photo_print_mat_list,
                'Материал для печати книг': print_mat_list
            }
            self.show_calc_info(complex_dict)


class get_day_calc_info(windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Количество продуктов за день")
        self.child_root.geometry("400x230")
        self.to_parent_center(root)
        self.book_calc_val = tk.StringVar()    # Переменная для хранения информации для книг по типам
        self.photo_calc_val = tk.StringVar()   # Переменная для общей суммы для фотопечати
        self.summ_info = tk.StringVar()
        self.__show_widgets()

    def __show_widgets(self):
        ask_order_lbl = tk.Label(self.child_root, text="Выберете день для подсчета")
        ask_order_lbl.place(x=6, y=2)
        self.start_date_combo = Combobox(self.child_root, values=self.__get_date_period(), state="readonly")
        self.start_date_combo.place(x=12, y=24)
        get_order_inf_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                      text='Посчитать', command=self.__main)
        get_order_inf_btn.place(x=180, y=20)
        separate_canvas = tk.Canvas(self.child_root, bg='black', height=1, width=400)
        separate_canvas.place(x=0, y=48)
        # Лейбл для вывода информации о заказе
        type_calc_frame = tk.Frame(self.child_root, width=396, height=155)
        type_calc_frame.place(x=2, y=52)
        book_calc_inf = tk.Label(type_calc_frame, textvariable=self.book_calc_val, justify=tk.LEFT)
        book_calc_inf.grid(row=0, column=0, sticky=tk.NW)
        photo_calc_info = tk.Label(type_calc_frame, textvariable=self.photo_calc_val, justify=tk.LEFT)
        photo_calc_info.grid(row=1, column=0, sticky=tk.NW)
        summ_lbl = tk.Label(type_calc_frame, textvariable=self.summ_info, justify=tk.LEFT)
        summ_lbl.grid(row=0, rowspan=2, column=1, sticky=tk.NW, ipadx=50)
        exit_btn = tk.Button(self.child_root, text="Закрыть", relief=tk.FLAT, fg="#eee", bg="#454545",
                             command=self.child_root.destroy)
        exit_btn.place(x=340, y=200)
        self.child_root.focus_set()
        self.child_root.grab_set()
        self.child_root.wait_window()

    @staticmethod
    def __get_date_period() -> list:
        # Получаем список дней доступных для подсчета периода. Сортируем по возрастанию (на всякий случай)
        log_lib = config.read_json_orders_log()
        period_list = []
        for name in log_lib:
            order_date = log_lib[name]['creation_date']
            if order_date not in period_list:
                period_list.append(order_date)
        return sorted(period_list)

    def __calc_cover_type(self, order_log):
        date_to_calc = self.start_date_combo.get()
        cover_type_dict = {
            "Книги": 0,
            "Планшеты": 0,
            "Альбомы": 0,
            "Дуо и Трио": 0
        }
        lf_plan_list = ("Фотокнига полиграфическая Layflat 20x30 верт 2-4 разворота",
                        "Фотокнига Layflat 20x30 верт су 1 мм 2-4 разворота",
                        "Фотокнига полиграфическая Layflat 25x25 2-4 разворота")
        for name in order_log:
            # Проверяем, что заказ соответствует выбранному дню
            if date_to_calc == order_log[name]['creation_date']:
                for product_name in order_log[name]['content']:
                    product_dict = order_log[name]['content'][product_name]
                    # Проверяем, что заказ не пустой и у него определен тип.
                    if product_dict['counts'] and product_dict['type']:
                        cover_count = product_dict['counts'][0]
                        product_type = product_dict['type'][0]
                        ob_name = product_dict['type'][1]
                        match product_type:
                            case "Фотокнига Стандарт" | "Фотокнига Классик" | "Фотокнига ЛЮКС" | "Фотокнига Flex Bind":
                                cover_type_dict['Книги'] += cover_count
                            case "Фотопланшет Стандарт":
                                cover_type_dict['Планшеты'] += cover_count
                            case "Layflat":
                                if ob_name in lf_plan_list:
                                    cover_type_dict['Планшеты'] += cover_count
                                else:
                                    cover_type_dict['Книги'] += cover_count
                            case "Фотоальбом полиграфический" | "Фотоальбом PUR":
                                cover_type_dict['Альбомы'] += cover_count
                            case "Фотопапка":
                                cover_type_dict['Дуо и Трио'] += cover_count
        # Сортируем словарь и очищаем от 0 значений
        sorted_dict = {}
        sorted_keys = sorted(cover_type_dict, key=cover_type_dict.get, reverse=True)
        for name in sorted_keys:
            if cover_type_dict[name] != 0:
                sorted_dict.update({name: cover_type_dict[name]})
        type_calc_inf = '\n'.join(f"{key}: {value}" for key, value in sorted_dict.items())
        type_calc_inf = "Итого:\n" + type_calc_inf
        self.summ_info.set(type_calc_inf)

    def __main(self):
        # Проверяем, что оба значения введены в комбобокс
        date_to_calc = self.start_date_combo.get()
        if date_to_calc:
            order_log = config.read_json_orders_log()
            product_count_dict = {
                "Фотокнига Стандарт": 0,
                "Фотокнига ЛЮКС": 0,
                "Фотокнига Flex Bind": 0,
                "Фотокнига Классик": 0,
                "Фотопланшет Стандарт": 0,
                "Layflat": 0,
                "Фотоальбом полиграфический": 0,
                "Фотоальбом PUR": 0,
                "Фотопапка": 0,
                "Фотожурнал": 0
            }
            photo_count_dict = {'Фотопечать': 0}
            for name in order_log:
                # Проверяем на соответствие дат введеным ограничениям.
                # Получаем словари для заказов
                if date_to_calc == order_log[name]['creation_date']:
                    for product_name in order_log[name]['content']:
                        product_dict = order_log[name]['content'][product_name]
                        # Проверяем, что заказ не пустой и у него определен тип.
                        if product_dict['counts'] and product_dict['type']:
                            # Для наглядности записываем в переменные значения количества и тип
                            product_type = product_dict['type'][0]
                            # Проверяем, что тип есть в словаре для вывода информации
                            if product_type in product_count_dict:
                                # Обновляем словарь полученной информацией из заказа
                                product_count_dict[product_dict['type'][0]] += product_dict['counts'][0]
                        if product_name == 'PHOTO' and product_dict['counts']:
                            photo_format_list = product_dict['counts']
                            for line in photo_format_list:
                                for val in line:
                                    photo_count_dict['Фотопечать'] += line[val]
            # Очищаем список от нулевых значений
            list_to_del = [prod_to_del for prod_to_del in product_count_dict if product_count_dict[prod_to_del] == 0]
            for line in list_to_del:
                del product_count_dict[line]
            # Сортируем список по количеству элементов
            sorted_dict = {}
            sorted_keys = sorted(product_count_dict, key=product_count_dict.get, reverse=True)
            for name in sorted_keys:
                sorted_dict.update({name: product_count_dict[name]})
            # Записываем полученную информацию в переменную
            inf_to_show = '\n'.join(f"{key}: {value}" for key, value in sorted_dict.items())
            self.book_calc_val.set(inf_to_show.lstrip('\n'))
            photo_info_to_show = ''.join(f"{key}: {value}" for key, value in photo_count_dict.items())
            self.photo_calc_val.set(photo_info_to_show)
            self.__calc_cover_type(order_log)


class get_period_calc_info(windows.child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Количество продуктов за период")
        self.child_root.geometry("220x350")
        self.to_parent_center(root)
        # Переменные для чекбатонов
        self.fb_std_val = tk.IntVar()
        self.fb_luxe_val = tk.IntVar()
        self.fb_fb_val = tk.IntVar()
        self.fb_class_val = tk.IntVar()
        self.fb_plan_val = tk.IntVar()
        self.fb_lf_val = tk.IntVar()
        self.fb_alb_val = tk.IntVar()
        self.fb_pur_val = tk.IntVar()
        self.fb_jur_val = tk.IntVar()
        self.fb_pap_val = tk.IntVar()
        self.foto_val = tk.IntVar()
        self.__show_date_period_widgets()
        self.__show_check_button_widgets()
        self.__show_button_widgets()
        self.child_root.focus_set()
        self.child_root.grab_set()
        self.child_root.wait_window()

    def __show_date_period_widgets(self):
        ask_order_lbl = tk.Label(self.child_root, text="Укажите период для подсчета")
        ask_order_lbl.place(x=6, y=2)
        start_date_lbl = tk.Label(self.child_root, text='C:')
        start_date_lbl.place(x=12, y=25)
        self.start_date_combo = Combobox(self.child_root, values=self.__get_date_period(), state="readonly")
        self.start_date_combo.place(x=30, y=24)
        end_date_lbl = tk.Label(self.child_root, text="По:")
        end_date_lbl.place(x=5, y=51)
        self.end_date_combo = Combobox(self.child_root, values=self.__get_date_period(), state="readonly")
        self.end_date_combo.place(x=30, y=50)

    def __show_check_button_widgets(self):
        separate_canvas = tk.Canvas(self.child_root, bg='black', height=1, width=400)
        separate_canvas.place(x=0, y=73)
        ask_product_type_lbl = tk.Label(self.child_root, text='Укажите категории для подсчета')
        ask_product_type_lbl.place(x=2, y=76)
        fb_std_cb = tk.Checkbutton(self.child_root, text='Фотокнига Стандарт', variable=self.fb_std_val)
        fb_std_cb.place(x=2, y=96)
        fb_std_cb.select()
        fb_luxe_cb = tk.Checkbutton(self.child_root, text='Фотокнига ЛЮКС', variable=self.fb_luxe_val)
        fb_luxe_cb.place(x=2, y=116)
        fb_luxe_cb.select()
        fb_fb_cb = tk.Checkbutton(self.child_root, text='Фотокнига Flex Bind', variable=self.fb_fb_val)
        fb_fb_cb.place(x=2, y=136)
        fb_fb_cb.select()
        fb_class_cb = tk.Checkbutton(self.child_root, text='Фотокнига Классик', variable=self.fb_class_val)
        fb_class_cb.place(x=2, y=156)
        fb_class_cb.select()
        fb_plan_cb = tk.Checkbutton(self.child_root, text='Планшет Стандарт', variable=self.fb_plan_val)
        fb_plan_cb.place(x=2, y=176)
        fb_plan_cb.select()
        fb_lf_cb = tk.Checkbutton(self.child_root, text='Фотокнига Layflat', variable=self.fb_lf_val)
        fb_lf_cb.place(x=2, y=196)
        fb_lf_cb.select()
        fb_alb_cb = tk.Checkbutton(self.child_root, text='Фотоальбом полиграфический', variable=self.fb_alb_val)
        fb_alb_cb.place(x=2, y=216)
        fb_alb_cb.select()
        fb_pur_cb = tk.Checkbutton(self.child_root, text='Фотоальбом PUR', variable=self.fb_pur_val)
        fb_pur_cb.place(x=2, y=236)
        fb_pur_cb.select()
        fb_jur_cb = tk.Checkbutton(self.child_root, text='Фотожурнал', variable=self.fb_jur_val)
        fb_jur_cb.place(x=2, y=256)
        fb_jur_cb.select()
        fb_pap_cb = tk.Checkbutton(self.child_root, text='Фотопапки Дуо и Трио', variable=self.fb_pap_val)
        fb_pap_cb.place(x=2, y=276)
        fb_pap_cb.select()
        fotoprint_cb = tk.Checkbutton(self.child_root, text='Фотопечать', variable=self.foto_val)
        fotoprint_cb.place(x=2, y=296)

    def __show_button_widgets(self):
        calc_button = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                text='Посчитать', command=self.main)
        calc_button.place(x=2, y=320)
        exit_button = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                text='Закрыть', command=self.child_root.destroy)
        exit_button.place(x=161, y=320)

    @staticmethod
    def __get_date_period() -> list:
        # Получаем список дней доступных для подсчета периода. Сортируем по возрастанию (на всякий случай)
        log_lib = config.read_json_orders_log()
        period_list = []
        for name in log_lib:
            order_date = log_lib[name]['creation_date']
            if order_date not in period_list:
                period_list.append(order_date)
        return sorted(period_list)

    def __check_and_get_period_values(self):
        # Получаем значения и проверяем, что период указан в правильной последовательности. Елси нет - переворачиваем
        start_date = self.start_date_combo.get()
        end_date = self.end_date_combo.get()
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        return start_date, end_date

    def __check_and_get_cb_values(self) -> list:
        type_list = []
        if self.fb_std_val.get() == 1:
            type_list.append("Фотокнига Стандарт")
        if self.fb_luxe_val.get() == 1:
            type_list.append("Фотокнига ЛЮКС")
        if self.fb_fb_val.get() == 1:
            type_list.append("Фотокнига Flex Bind")
        if self.fb_class_val.get() == 1:
            type_list.append("Фотокнига Классик")
        if self.fb_plan_val.get() == 1:
            type_list.append("Фотопланшет Стандарт")
        if self.fb_lf_val.get() == 1:
            type_list.append("Layflat")
        if self.fb_alb_val.get() == 1:
            type_list.append("Фотоальбом полиграфический")
        if self.fb_pur_val.get() == 1:
            type_list.append("Фотоальбом PUR")
        if self.fb_jur_val.get() == 1:
            type_list.append("Фотожурнал")
        if self.fb_pap_val.get() == 1:
            type_list.append("Фотопапка")
        if self.foto_val.get() == 1:
            type_list.append("Фотопечать")
        return type_list

    def main(self):
        # Получаем период и категории продуктов для подсчета
        datas_tuple = self.__check_and_get_period_values()
        type_list = self.__check_and_get_cb_values()
        if datas_tuple[0] and datas_tuple[1] and type_list:
            # Получаем лог заказов
            order_log = config.read_json_orders_log()
            complex_dict = {}
            product_dict = {name: 0 for name in type_list}
            # Формируем заготовку для словаря
            for name in order_log:
                creation_date = order_log[name]['creation_date']
                if datas_tuple[0] <= creation_date <= datas_tuple[1]:
                    if creation_date not in complex_dict:
                        value = {creation_date: product_dict.copy()}
                        complex_dict.update(value)
                if creation_date > datas_tuple[1]:
                    break
            # Наполняем заготовку значениями
            for name in order_log:
                creation_date = order_log[name]['creation_date']
                if datas_tuple[0] <= creation_date <= datas_tuple[1]:
                    # Пробегаемся по контенту заказа
                    order_content = order_log[name]['content']
                    for product in order_content:
                        # Проверяем на реальность заказа
                        if order_content[product]['type'] and order_content[product]['counts']:
                            cover_count = order_content[product]['counts'][0]
                            product_type = order_content[product]['type'][0]
                            # Проверяем, что тип продукта есть в заготовке
                            if product_type in type_list:
                                complex_dict[creation_date][product_type] += cover_count
                        if product == 'PHOTO' and order_content[product]['counts'] and 'Фотопечать' in type_list:
                            cover_count = order_content[product]['counts']
                            cover_count = sum([val for name in cover_count for val in name.values()])
                            complex_dict[creation_date]['Фотопечать'] += cover_count
            get_grap.show_graphics(complex_dict)
