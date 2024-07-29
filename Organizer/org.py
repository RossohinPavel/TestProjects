import tkinter as tk

import Data.windows as windows
import Data.roddom as roddom
import Data.processing as proc
import Data.log as log
import Data.Book_lib as Book_lib
import Data.get_order_info as get_oi


class main_window:
    # Основные настройки окна
    def __init__(self):
        self.root = tk.Tk()
        self.__to_screen_center()
        self.__show_main_widgets()
        self.root.title("Органайзер")
        # self.root.iconbitmap('Data/ico/ico1.ico')
        self.root.attributes("-alpha", 0.98)

    # Размер и положение окна
    def __to_screen_center(self):
        width = 270
        height = 520
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        screen_width = (screen_width - width) // 2
        screen_height = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{screen_width}+{screen_height}")
        self.root.resizable(False, False)

    # Меню бар
    def __show_menu(self):

        def show_pic_processing_window(): windows.settings_window(self.root)

        settings_menu = tk.Menu(tearoff=0)
        settings_menu.add_command(label="Общие настройки", command=show_pic_processing_window)

        main_menu = tk.Menu()
        main_menu.add_cascade(label="Настройки", menu=settings_menu)
        self.root.config(menu=main_menu)

    # Основные фреймы
    def __main_frame(self):
        # Запуск лога и генератор наклеек

        def init_log(): log.New_Log_Creator().main()

        def init_stickgen(): get_oi.Get_sticker(self.root)

        def init_order_mat(): get_oi.get_order_material(self.root)

        def init_period_mat(): get_oi.get_period_material(self.root)

        def init_product_calc_day(): get_oi.get_day_calc_info(self.root)

        def init_product_calc_period(): get_oi.get_period_calc_info(self.root)

        def show_information_menu():
            btn_x = mat_frame.winfo_rootx()
            btn_y = mat_frame.winfo_rooty()
            inf_menu = tk.Menu(tearoff=0)
            inf_menu.add_command(label='Расход материала для заказа', command=init_order_mat)
            inf_menu.add_command(label="Расход материала для периода", command=init_period_mat)
            inf_menu.add_command(label="Количество продуктов за день", command=init_product_calc_day)
            inf_menu.add_command(label="Количество продуктов за период", command=init_product_calc_period)
            inf_menu.post(x=btn_x+115, y=btn_y+30)

        def show_blib_add_window(): Book_lib.show_add_window(self.root)
        def show_blib_change_window(): Book_lib.show_change_window(self.root)
        def show_blib_delete_window(): Book_lib.show_delete_window(self.root)

        def show_lib_menu():
            btn_x = mat_frame.winfo_rootx()
            btn_y = mat_frame.winfo_rooty()
            book_lib_menu = tk.Menu(tearoff=0)
            book_lib_menu.add_command(label="Добавить", command=show_blib_add_window)
            book_lib_menu.add_command(label="Изменить", command=show_blib_change_window)
            book_lib_menu.add_command(label="Удалить", command=show_blib_delete_window)
            book_lib_menu.post(x=btn_x+10, y=btn_y+30)

        log_frame = windows.Frame_on_Main_window()
        log_frame.add_label(color="#ed95b7", text="Работа с заказами")
        log_frame.add_l_button(text="Обновить бд", command=init_log, padx=20)
        log_frame.add_r_button(text="СтикГен", command=init_stickgen, padx=30)
        mat_frame = windows.Frame_on_Main_window()
        mat_frame.add_r_button(text="Информация", command=show_information_menu, padx=10)
        mat_frame.add_l_button(text="Библиотека", command=show_lib_menu, padx=20)

        # Книги на фотобумаге

        def init_to_canal(): proc.foto_book(self.root)

        fotopaper_book_frame = windows.Frame_on_Main_window()
        fotopaper_book_frame.add_label(color='light goldenrod', text="Книги на фотобумаге")
        fotopaper_book_frame.add_button(text="Подготовка к печати", command=init_to_canal)

        # Полиграфические заказы

        def init_poli(): proc.poli_book(self.root)

        poli_book = windows.Frame_on_Main_window()
        poli_book.add_label(color='dark salmon', text="Полиграфические книги")
        poli_book.add_button(text="Подготовка к печати", command=init_poli)

        def init_alb(): proc.poli_alb(self.root)

        poli_alb = windows.Frame_on_Main_window()
        poli_alb.add_label(color='dark salmon', text="Альбомы и пур")
        poli_alb.add_button(text="Подготовка к печати", command=init_alb)

        def init_jur(): proc.poli_jur(self.root)

        poli_jur = windows.Frame_on_Main_window()
        poli_jur.add_label(color='dark salmon', text="Журналы")
        poli_jur.add_button(text="Подготовка к печати", command=init_jur)

        # Бакап заказа
        def init_bup(): proc.simple_buckup(self.root)

        another_frame = windows.Frame_on_Main_window()
        another_frame.add_label(color='#adc6ed', text='Остальное')
        another_frame.add_button(text='Бакап заказа', pad_x=2, command=init_bup)

        # Фотопечать
        def init_roddom(): roddom.Roddom(self.root).main(),

        frame_rd = windows.Frame_on_Main_window()
        frame_rd.add_label(color='pale green', text='Фотопечать')
        frame_rd.add_button(text="Роддом", command=init_roddom, pad_x=50,
                            tip="Посчитать и отправить в печать заказы роддома")

    # Отрисовка всех виджетов
    def __show_main_widgets(self):
        self.__show_menu()
        self.__main_frame()


if __name__ == "__main__":
    app = main_window()
    app.root.mainloop()
