import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import messagebox as tkmb

import os
import shutil

import Data.get_list as get_list
import Data.config as config
import Data.image_processing as im_proc


class window_for_processing:
    def __init__(self, root):
        self.cwfop = tk.Toplevel(root, relief='solid', border=1)
        self.cwfop.overrideredirect(True)
        self.cwfop.iconbitmap('Data/ico/ico1.ico')
        self.cwfop.geometry("300x120")
        self.cwfop.resizable(False, False)
        self.__to_parent_center(root)
        self.order_name_var = tk.StringVar(self.cwfop)
        self.__init_cb_values()
        self.__show_main_widgets()
        self.__show_processing_widgets()

    def __to_parent_center(self, root):  # Центрирование относительно основного окна
        self.cwfop.update_idletasks()
        calc_pos_x = ((root.winfo_width() - self.cwfop.winfo_width()) // 2)
        calc_pos_y = ((root.winfo_height() - self.cwfop.winfo_height()) // 2)
        place_x = root.winfo_x() + calc_pos_x + 8
        place_y = root.winfo_y() + calc_pos_y + 8
        self.cwfop.geometry(f"+{place_x}+{place_y}")

    def __init_cb_values(self):
        self.cs_cb_value = tk.IntVar()
        self.gl_cb_value = tk.IntVar()
        self.ren_cb_value = tk.IntVar()
        self.bp_cb_value = tk.IntVar()
        self.dc_cb_value = tk.IntVar()

    def __show_main_widgets(self):
        order_ask_lbl = tk.Label(self.cwfop, text="Введите номер заказа:")
        order_ask_lbl.place(x=85, y=40)
        self.order_name_entry = tk.Entry(self.cwfop, textvariable=self.order_name_var, width=20)
        self.order_name_entry.place(x=87, y=60)
        self.order_name_entry.focus_set()
        self.start_btn = tk.Button(self.cwfop, text="Запуск", relief=tk.FLAT, fg="#eee", bg="#454545")
        self.start_btn.place(x=190, y=91)
        cancel_btn = tk.Button(self.cwfop, relief=tk.FLAT, fg="#eee", bg="#454545",
                               text="Отмена", command=self.cwfop.destroy)
        cancel_btn.place(x=244, y=91)

    def __show_processing_widgets(self):
        self.operation_title_lbl = tk.Label(self.cwfop, text="Операция")
        self.order_line_lbl = tk.Label(self.cwfop, text="заказ")  # Тайтл для отображения заказа и тиража
        self.count_lbl = tk.Label(self.cwfop, text="Счетчик, файл")  # Тайтл для счетчика
        self.prog_bar = Progressbar(self.cwfop, mode="determinate", length=294)

    def show_cb_widgets(self, *args):
        if 'cs0' in args or 'cs1' in args:
            covers_stroke_cb = tk.Checkbutton(self.cwfop, text="Обводка обложек", variable=self.cs_cb_value)
            covers_stroke_cb.place(x=0, y=0)
            self.cs_cb_value.set(1 if 'cs1' in args else 0)
        if 'gl0' in args or 'gl1' in args:
            guideline_cb = tk.Checkbutton(self.cwfop, text="Направляющие", variable=self.gl_cb_value)
            guideline_cb.place(x=0, y=18 if 'cs0' in args or 'cs1' in args else 0)
            self.gl_cb_value.set(1 if 'gl1' in args else 0)
        if 'ren0' in args or 'ren1' in args:
            rename_cb = tk.Checkbutton(self.cwfop, text="Переименование", variable=self.ren_cb_value)
            rename_cb.place(x=150, y=0)
            self.ren_cb_value.set(1 if 'ren1' in args else 0)
        if 'bp0' in args or 'bp1' in args:
            bp_cb = tk.Checkbutton(self.cwfop, text="Добавить БекПринт", variable=self.bp_cb_value)
            bp_cb.place(x=150, y=18)
            self.bp_cb_value.set(1 if 'bp1' in args else 0)
        if 'dc0' in args or 'dc1' in args:
            decoding_cb = tk.Checkbutton(self.cwfop, text='Раскодировка', variable=self.dc_cb_value)
            decoding_cb.place(x=150, y=0)
            self.dc_cb_value.set(1 if 'dc1' in args else 0)

    def check_order_name(self) -> tuple:
        order_name = self.order_name_var.get()
        order_dict = config.read_json_orders_log()
        if order_name in order_dict:
            for widget in self.cwfop.winfo_children():
                if widget.winfo_name() not in ('!button2', '!label2', '!label3', '!label4', '!progressbar'):
                    widget.destroy()
            self.operation_title_lbl.place(x=2, y=2)
            self.order_line_lbl.place(x=2, y=24)
            self.count_lbl.place(x=2, y=46)
            self.prog_bar.place(x=2, y=68)
            return order_name, order_dict[
                order_name], self.cs_cb_value.get(), self.gl_cb_value.get(), self.ren_cb_value.get(), self.bp_cb_value.get(), self.dc_cb_value.get()
        else:
            self.order_name_entry.delete(0, tk.END)
            tkmb.showwarning(title="Ошибка", message="Введен неверный номер заказа")

    @staticmethod
    def get_content_files(order_dict: dict, *args: str) -> dict:
        file_dict = {}
        book_lib = config.read_json_book_lib()
        path = order_dict['path']
        for name in order_dict['content']:
            if order_dict['content'][name]['counts'] and order_dict['content'][name]['type']:
                prod_class = order_dict['content'][name]['type'][0]
                prod_type = order_dict['content'][name]['type'][1]
                if prod_class in args:
                    file_list = get_list.new_ex_list(f'{path}/{name}')
                    file_list = {'file_list': file_list}
                    prod_dict = book_lib[prod_class][prod_type]
                    file_list.update(prod_dict)
                    file_dict.update({name: file_list})
        if file_dict:
            return file_dict

    @staticmethod
    def file_counter(file_dict) -> int:
        counter = 0
        for name in file_dict:
            for ex in file_dict[name]['file_list']:
                counter += len(ex) - 1
        return counter

    @staticmethod
    def ex_counter(file_dict) -> int:
        counter = 0
        for name in file_dict:
            counter += len(file_dict[name]['file_list'])
        return counter


    def focus(self):
        self.cwfop.grab_set()
        self.cwfop.wait_window()


class simple_buckup(window_for_processing):
    def __init__(self, root):
        super().__init__(root)
        self.operation_title_lbl.config(text="Бакап заказа")
        self.start_btn.config(command=self.main)
        self.order_name_entry.bind("<Return>", self.main)
        self.focus()

    def main(self, event=None):
        try:
            order_tuple = self.check_order_name()
            if order_tuple:
                order_name = order_tuple[0]
                path = order_tuple[1]['path']
                file_list = get_list.simple_list(path)
                os.makedirs(f'{path}\\_TO_PRINT', exist_ok=True)
                file_total_count = len(file_list)
                file_count_to_minus = file_total_count
                self.prog_bar['maximum'] = file_total_count
                self.prog_bar['value'] = 0
                self.cwfop.update()
                dir_to_cr = []
                for line in file_list:
                    splited_line = line.split('\\')
                    if len(splited_line) > 1:
                        current_dir_seq = splited_line[:-1:]
                        if current_dir_seq != dir_to_cr:
                            current_dir_seq = '/'.join(current_dir_seq)
                            os.makedirs(f'{path}\\_TO_PRINT\\{current_dir_seq}', exist_ok=True)
                            dir_to_cr = splited_line[:-1:]
                    self.order_line_lbl.config(text=f"{order_name} / {dir_to_cr[0] if dir_to_cr else ''}")
                    shutil.copy2(f'{path}\\{line}', f'{path}\\_TO_PRINT\\{line}')
                    file_count_to_minus -= 1
                    self.count_lbl.config(text=f"{file_total_count}/{file_count_to_minus} -- {splited_line[-1]}")
                    self.prog_bar['value'] += 1
                    self.cwfop.update()
                self.cwfop.destroy()
        except tk.TclError:
            tkmb.showerror(title="Остановка обработки", message='Остановлено по требованию пользователя')


class poli_jur(window_for_processing):
    def __init__(self, root):
        super().__init__(root)
        self.operation_title_lbl.config(text="Обработка Журналов")
        self.start_btn.config(command=self.main)
        self.order_name_entry.bind("<Return>", self.main)
        self.show_cb_widgets('dc0')
        self.focus()

    def main(self, event=None):
        order_tuple = self.check_order_name()
        if order_tuple:
            try:
                decoding = order_tuple[6]
                file_dict = self.get_content_files(order_tuple[1], 'Фотожурнал')
                order_name = order_tuple[0]
                path = order_tuple[1]['path']
                if file_dict:
                    total_count = self.ex_counter(file_dict)
                    minus_count = total_count
                    self.prog_bar['maximum'] = total_count
                    self.prog_bar['value'] = 0
                    self.cwfop.update()
                    for name in file_dict:
                        self.order_line_lbl.config(text=f"{order_name} / {name}")
                        for ex in file_dict[name]['file_list']:
                            self.count_lbl.config(text=f"{total_count}/{minus_count} -- {ex[0]}")
                            self.cwfop.update()
                            ex_src = f'{path}/{name}/{ex[0]}'
                            ex_dest = f'{path}/_TO_PRINT/{name}/{ex[0]}'
                            os.makedirs(ex_dest, exist_ok=True)
                            pages = ex[1::]
                            if decoding == 1:
                                im_proc.journal_decoding(ex[1::], ex_src, ex_dest)
                            else:
                                for file in pages:
                                    shutil.copy2(f'{ex_src}/{file}', ex_dest)
                            minus_count -= 1
                            self.prog_bar['value'] += 1
                self.cwfop.destroy()
            except tk.TclError:
                tkmb.showerror(title="Остановка обработки", message='Остановлено по требованию пользователя')


class poli_alb(window_for_processing):
    def __init__(self, root):
        super().__init__(root)
        self.operation_title_lbl.config(text="Обработка Альбомов")
        self.start_btn.config(command=self.main)
        self.order_name_entry.bind("<Return>", self.main)
        self.show_cb_widgets('gl0', 'dc0')
        self.focus()

    def main(self, event=None):
        order_tuple = self.check_order_name()
        if order_tuple:
            try:
                img_config = config.read_section('IMAGE')
                guideline = order_tuple[3]
                decoding = order_tuple[6]
                file_dict = self.get_content_files(order_tuple[1], 'Фотоальбом полиграфический', "Фотоальбом PUR")
                order_name = order_tuple[0]
                path = order_tuple[1]['path']
                if file_dict:
                    total_count = self.ex_counter(file_dict)
                    minus_count = total_count
                    self.prog_bar['maximum'] = total_count
                    self.prog_bar['value'] = 0
                    self.cwfop.update()
                    for name in file_dict:
                        self.order_line_lbl.config(text=f"{order_name} / {name}")
                        os.makedirs(f'{path}/_TO_PRINT/{name}/Covers', exist_ok=True)
                        os.makedirs(f'{path}/_TO_PRINT/{name}/Pages', exist_ok=True)
                        spine = int(file_dict[name]['spine'])
                        for ex in file_dict[name]['file_list']:
                            self.count_lbl.config(text=f"{total_count}/{minus_count} -- {ex[0]}")
                            self.cwfop.update()
                            cover = ex[-1]
                            cover_src = f'{path}/{name}/{ex[0]}/{cover}'
                            if guideline == 1:
                                im_proc.cover_processing(file_source=cover_src,
                                                         file_dest=f'{path}/_TO_PRINT/{name}/Covers', file_name=cover,
                                                         gl_size=int(img_config['guideline_size']),
                                                         gl_color=img_config['guideline_color'],
                                                         gl_lengh=90, gl_spine=spine, luxe=False)
                            else:
                                shutil.copy2(cover_src, f'{path}/_TO_PRINT/{name}/Covers')
                            pages = ex[1:-1:]
                            pages_len = len(pages)
                            pages_dest = f'{path}/_TO_PRINT/{name}/Pages/{pages_len}p_{ex[0]}'
                            os.makedirs(pages_dest,  exist_ok=True)
                            if decoding == 1:
                                im_proc.album_decoding(pages, f'{path}/{name}/{ex[0]}', pages_dest, ex[0])
                            else:
                                for file in pages:
                                    src = f'{path}/{name}/{ex[0]}/{file}'
                                    shutil.copy2(src, f'{pages_dest}/{file}')
                            minus_count -= 1
                            self.prog_bar['value'] += 1
                self.cwfop.destroy()
            except tk.TclError:
                tkmb.showerror(title="Остановка обработки", message='Остановлено по требованию пользователя')


class poli_book(window_for_processing):
    def __init__(self, root):
        super().__init__(root)
        self.operation_title_lbl.config(text="Обработка Layflat")
        self.start_btn.config(command=self.main)
        self.order_name_entry.bind("<Return>", self.main)
        self.show_cb_widgets('gl0', 'ren0')
        self.focus()

    def main(self, event=None):
        order_tuple = self.check_order_name()
        if order_tuple:
            try:
                img_config = config.read_section('IMAGE')
                guideline = order_tuple[3]
                rename = order_tuple[4]
                order_name = order_tuple[0]
                path = order_tuple[1]['path']
                file_dict = self.get_content_files(order_tuple[1], "Layflat")
                if file_dict:
                    total_count = self.file_counter(file_dict)
                    minus_count = total_count
                    self.prog_bar['maximum'] = total_count
                    self.prog_bar['value'] = 0
                    self.cwfop.update()
                    prod_count = 0
                    for name in file_dict:
                        self.order_line_lbl.config(text=f"{order_name} / {name}")
                        cov_dir = f'{path}/_TO_PRINT/{name}/Covers'
                        page_dir = f'{path}/_TO_PRINT/{name}/Variable'
                        os.makedirs(cov_dir, exist_ok=True)
                        os.makedirs(page_dir, exist_ok=True)
                        # Технические переменные
                        prod_count += 1
                        spine = int(file_dict[name]['spine'])
                        option = 'бу' if file_dict[name]['book_option'] == 'б/у' else 'су'
                        for ex in file_dict[name]['file_list']:
                            page_count = len(ex) - 2
                            cover = ex[-1].split('.')[0]
                            cover_name = f"{cover}.jpg" if rename == 0 else f"{prod_count}_{cover}_{page_count}{option}.jpg"
                            self.count_lbl.config(text=f"{total_count}/{minus_count} -- {cover}")
                            if guideline == 1 and spine > 0:
                                im_proc.cover_processing(file_source=f'{path}/{name}/{ex[0]}/{cover}.jpg',
                                                         file_dest=cov_dir, file_name=cover_name,
                                                         gl_size=int(img_config['guideline_size']),
                                                         gl_color=img_config['guideline_color'],
                                                         gl_lengh=90, gl_spine=spine, luxe=False)
                            else:
                                shutil.copy2(f'{path}/{name}/{ex[0]}/{cover}.jpg',
                                             f'{path}/_TO_PRINT/{name}/Covers/{cover_name}')
                            minus_count -= 1
                            self.prog_bar['value'] += 1
                            self.cwfop.update()
                            for page in ex[1:-1:]:
                                self.count_lbl.config(text=f"{total_count}/{minus_count} -- {page}")
                                splited_name = page.split('.')[0]
                                page_name = f'{splited_name}.jpg' if rename == 0 else f'{prod_count}_{splited_name}.jpg'
                                shutil.copy2(f'{path}/{name}/{ex[0]}/{page}', f'{page_dir}/{page_name}')
                                minus_count -= 1
                                self.prog_bar['value'] += 1
                                self.cwfop.update()
                self.cwfop.destroy()
            except tk.TclError:
                tkmb.showerror(title="Остановка обработки", message='Остановлено по требованию пользователя')


class foto_book(window_for_processing):
    def __init__(self, root):
        super().__init__(root)
        self.operation_title_lbl.config(text="Обработка Фотокниг на фотобумаге")
        self.start_btn.config(command=self.main)
        self.order_name_entry.bind("<Return>", self.main)
        self.show_cb_widgets('cs1', 'gl1', 'ren0', 'bp0')
        self.focus()

    def main(self, event=None):
        order_tuple = self.check_order_name()
        if order_tuple:
            try:
                img_config = config.read_section('IMAGE')
                stroke = order_tuple[2]
                guideline = order_tuple[3]
                rename = order_tuple[4]
                back_print = order_tuple[5]
                order_name = order_tuple[0]
                path = order_tuple[1]['path']
                file_dict = self.get_content_files(order_tuple[1], "Фотокнига Стандарт", "Фотокнига ЛЮКС",
                                                   "Фотокнига Классик", "Фотопланшет Стандарт")
                if file_dict:
                    total_count = self.file_counter(file_dict)
                    minus_count = total_count
                    self.prog_bar['maximum'] = total_count
                    self.prog_bar['value'] = 0
                    self.cwfop.update()
                    prod_count = 0
                    for name in file_dict:
                        prod_count += 1
                        self.order_line_lbl.config(text=f"{order_name} / {name}")
                        cov_dir = f'{path}/_TO_PRINT/{name}/{file_dict[name]["cover_canal"]}'
                        page_dir = f'{path}/_TO_PRINT/{name}/{file_dict[name]["page_canal"]}'
                        os.makedirs(cov_dir, exist_ok=True)
                        os.makedirs(page_dir, exist_ok=True)
                        prod_dict = {}
                        if stroke == 1 and file_dict[name]["cover_canal"] != 'poli':
                            prod_dict.update({'s_size': int(img_config['stroke_size']),
                                              's_color': img_config['stroke_color']})
                        if guideline == 1 and 'spine' in file_dict[name] and int(file_dict[name]['spine']) > 0:
                            prod_dict.update({'luxe': True if file_dict[name]['short_name'] == 'Люкс' else False,
                                              'gl_size': int(img_config['guideline_size']),
                                              'gl_color': img_config['guideline_color'],
                                              'gl_lengh': 90, 'gl_spine': int(file_dict[name]['spine'])})
                        option = ''
                        bp_option = ''
                        if rename == 1:
                            bp_option = file_dict[name]['book_option']
                            if bp_option == 'б/у':
                                option = 'bu'
                            elif bp_option == 'с/у':
                                option = 'cu'
                            else:
                                option = 'cu1.2'
                        for ex in file_dict[name]['file_list']:
                            cover = ex[-1]
                            cover_name = cover if rename == 0 else f"{prod_count}_{cover.split('.')[0]}_{len(ex) - 2}{option}.jpg"
                            pages = ex[1:-1:]
                            if back_print == 1 and file_dict[name]["cover_canal"] != 'poli':
                                bp_name = cover_name
                                if rename == 1:
                                    bp_name = f"{order_name}_{prod_count}_{cover.split('.')[0]}_{len(ex) - 2}{bp_option}.jpg"
                                prod_dict.update({'back_print': bp_name})
                            self.count_lbl.config(text=f"{total_count}/{minus_count} -- {cover}")
                            if prod_dict:
                                im_proc.cover_processing(file_source=f'{path}/{name}/{ex[0]}/{cover}',
                                                         file_dest=cov_dir, file_name=cover_name, **prod_dict)
                            else:
                                shutil.copy2(f'{path}/{name}/{ex[0]}/{cover}', f'{cov_dir}/{cover_name}')
                            minus_count -= 1
                            self.prog_bar['value'] += 1
                            self.cwfop.update()
                            for page in pages:
                                self.count_lbl.config(text=f"{total_count}/{minus_count} -- {page}")
                                page_name = page if rename == 0 else f'{option}_{prod_count}_{page.split(".")[0]}.jpg'
                                shutil.copy2(f'{path}/{name}/{ex[0]}/{page}', f'{page_dir}/{page_name}')
                                minus_count -= 1
                                self.prog_bar['value'] += 1
                                self.cwfop.update()
                self.cwfop.destroy()
            except tk.TclError:
                tkmb.showerror(title="Остановка обработки", message='Остановлено по требованию пользователя')
