import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import messagebox as tkmb
from tkinter.ttk import Progressbar

import os
import re
import shutil

import Data.windows as windows
import Data.config as config
import Data.get_list as get_list


class Roddom(windows.child_window):
    # Модуль для обработки заказов роддома. Простой функционал: Подсчет файлов и отправка подсчитанного заказа в печать.
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title("Роддом - обработка заказов")
        self.child_root.geometry("259x210")
        self.to_parent_center(root)
        self.working_dir = config.read_section("working_dir")  # Словарь рабочих папок
        # Фрейм для отрисовки ИЛИ вывода прогрессбара.
        self.calc_or_progress_frame = tk.Frame(self.child_root, width=254, height=80)
        self.calc_or_progress_frame.place(x=2, y=65)
        # Переменная для хранения посчитанной информации. По ней осуществляем проверку, что заказ посчитан.
        self.calc_order_dir = None

    def __clear_info_or_prog_frame(self):
        for widget in self.calc_or_progress_frame.winfo_children():
            widget.destroy()

    def __init_count(self):
        # Очищаем фрейм отображения информации
        self.__clear_info_or_prog_frame()
        # Выбираем заказ для подсчета
        calc_pap = tkfd.askdirectory(title="Выберете папку для подсчета",
                                     initialdir=self.working_dir['roddom_main_dir'])
        if calc_pap:
            # Вспомогательные переменные для подсчета
            num_15x21 = 0
            num_21x30 = 0
            num_9x15 = 0
            file_list = []
            # Вспомогательная переменная для вывода посчитанного заказа
            print_day_work = os.path.basename(calc_pap)
            # Пробегаемся по выпискам в заказе
            for root, dirs, files in os.walk(calc_pap):
                for file in files:
                    line = os.path.join(root, file)
                    rel_path = os.path.relpath(line, calc_pap)
                    file_list.append(rel_path)
            for name in file_list:
                name = name.split('\\')
                if len(name) == 3 and re.fullmatch(r'.+\.jpg', name[2]):
                    match name[1]:
                        case '15x21': num_15x21 += 1
                        case '21x30': num_21x30 += 1
                        case '9x15': num_9x15 += 1
            # Комплектуем информацию в F формате для записи в тхт файл и обображения на экране
            info_to_print = f'{print_day_work}\n{" " * 10}9x15  =  {num_9x15}' \
                            f'\n{" " * 10}15x21 =  {num_15x21}\n{" " * 10}21x30 =  {num_21x30}'
            with open(f"{calc_pap}/{print_day_work} - sum.txt", "w") as txtfile:
                txtfile.write(info_to_print)
            # Записываем информацию о посчитанном заказе
            self.calc_order_dir = calc_pap
            # Выводим информацию на экран
            calc_info_lbl = tk.Label(self.calc_or_progress_frame, text=info_to_print, font="Arial 12", justify=tk.LEFT)
            calc_info_lbl.place(x=10, y=0)
        else:
            # Принудительно очищаем переменные при ошибке или инициализации повторного подсчета
            self.calc_order_dir = None
            for widget in self.calc_or_progress_frame.winfo_children():
                widget.destroy()
            tkmb.showerror(title="Ошибка", message="Заказ не был посчитан")

    def __to_print(self):
        # Очищаем фрейм вывода информации
        self.__clear_info_or_prog_frame()
        if self.calc_order_dir is None:
            tkmb.showerror(title="Ошибка", message="Нужно посчитать заказ.")
        else:
            # Делаем выбор для папки, куда скопировать заказ на печать
            oper_disc = self.working_dir['fp_oper_disc']
            dest_dir = tkfd.askdirectory(title="Выберите папку, куда скопировать заказ", initialdir=oper_disc)
            if dest_dir:
                # Получаем название папка заказа для создания ее в том каталоге, куда  копируется
                pap_basename = os.path.basename(self.calc_order_dir)
                self.child_root.clipboard_clear()
                self.child_root.clipboard_append(f"{dest_dir}\n\nроддом\n\n{pap_basename}")
                zak_number_label = tk.Label(self.calc_or_progress_frame, text=pap_basename)
                zak_number_label.place(x=0, y=0)
                type_of_proc_label = tk.Label(self.calc_or_progress_frame, text="Получаю список файлов")
                type_of_proc_label.place(x=77, y=0)
                count_label = tk.Label(self.calc_or_progress_frame, text="Счетчик")
                count_label.place(x=0, y=15)
                file_label = tk.Label(self.calc_or_progress_frame, text="Файл")
                file_label.place(x=77, y=15)
                pb = Progressbar(self.calc_or_progress_frame, orient=tk.HORIZONTAL, mode="determinate", length=254)
                pb.place(x=0, y=36)
                list_to_copy = get_list.simple_list(self.calc_order_dir)
                type_of_proc_label.config(text="Обновляю информацию")
                main_lenght = len(list_to_copy)
                lenght_to_minus = main_lenght
                count_label.config(text=f"{main_lenght}/{lenght_to_minus}")
                pb['maximum'] = main_lenght
                pb['value'] = 0
                self.child_root.update()
                type_of_proc_label.config(text="Копирую файлы")
                # Блокируем нажатия на кнопки, чтобы не сбить выполнение
                self.to_print_btn.config(state="disabled")
                self.init_count_btn.config(state="disabled")
                os.makedirs(f'{dest_dir}\\{pap_basename}', exist_ok=True)
                dir_to_cr = []
                # Циклом копируем файлы
                for i in list_to_copy:
                    splited_line = i.split('\\')
                    if len(splited_line) > 1:
                        current_dir_seq = splited_line[:-1:]
                        if current_dir_seq != dir_to_cr:
                            current_dir_seq = '/'.join(current_dir_seq)
                            os.makedirs(f'{dest_dir}\\{pap_basename}\\{current_dir_seq}', exist_ok=True)
                            dir_to_cr = splited_line[:-1:]
                    shutil.copy2(f"{self.calc_order_dir}\\{i}",
                                 f"{dest_dir}\\{pap_basename}\\{i}")  # копируем файлы в эти директории
                    file_label.config(text=f"{splited_line[-1]}")  # Далее - для обновления информации на виджете
                    lenght_to_minus -= 1
                    count_label.config(text=f"{main_lenght}/{lenght_to_minus}")
                    pb['value'] += 1
                    self.child_root.update()
                type_of_proc_label.config(text="Завершено")
                self.to_print_btn.config(state="normal")
                self.init_count_btn.config(state="normal")
                self.calc_order_dir = None
                file_label.config(text="")
                self.child_root.update()
            else:
                self.calc_order_dir = None
                tkmb.showerror(title="Ошибка", message="Папка не выбрана")

    def __show_widget(self):
        roddom_main_dir_lbl = tk.Label(self.child_root, text="Папка, куда загружается роддом:")
        roddom_main_dir_lbl.place(x=2, y=4, anchor="nw")
        current_folder_lbl = tk.Label(self.child_root, justify=tk.LEFT, wraplength=260,
                                      text=self.working_dir['roddom_main_dir'])
        current_folder_lbl.place(x=2, y=30, height=30)
        canv1 = tk.Canvas(self.child_root, width=254, height=1, bg="black")
        canv1.place(y=60)
        canv2 = tk.Canvas(self.child_root, width=254, height=1, bg="black")
        canv2.place(y=144)
        self.init_count_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                        text="Посчитать заказ", command=self.__init_count)
        self.init_count_btn.place(x=2, y=149)
        self.to_print_btn = tk.Button(self.child_root, relief=tk.FLAT, fg="#eee", bg="#454545",
                                      text="Отправить в печать", command=self.__to_print)
        self.to_print_btn.place(x=138, y=149)
        destroy_btn = tk.Button(self.child_root, text="Закрыть", relief=tk.FLAT, fg="#eee", bg="#454545",
                                command=self.child_root.destroy)
        destroy_btn.place(x=199, y=180)

    def main(self):
        self.__show_widget()
        self.focus()
