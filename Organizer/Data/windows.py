import tkinter as tk
from tkinter import colorchooser as tkcc
from tkinter import filedialog as tkfd
from idlelib.tooltip import Hovertip

import Data.config as config


class child_window:
    def __init__(self, root, title=""):  # Параметры дочернего окна
        self.child_root = tk.Toplevel(root)
        self.child_root.title(title)
        # self.child_root.iconbitmap('Data/ico/ico1.ico')
        self.child_root.resizable(False, False)

    def to_parent_center(self, root):  # Центрирование относительно основного окна
        self.child_root.update_idletasks()
        parent_width = root.winfo_width()  # Получаем размер родительского окна
        parent_height = root.winfo_height()
        parent_place_x = root.winfo_x()  # Получаем положение родительского окна
        parent_place_y = root.winfo_y()
        child_width = self.child_root.winfo_width()  # Размер дочернего окна
        child_height = self.child_root.winfo_height()
        place_x = ((parent_width - child_width) // 2) + parent_place_x
        place_y = ((parent_height - child_height) // 2) + parent_place_y
        self.child_root.geometry(f"+{place_x}+{place_y}")

    def focus(self):  # функция фокуса
        self.child_root.grab_set()
        self.child_root.focus_set()
        self.child_root.wait_window()


class Frame_on_Main_window(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack(fill=tk.X)

    def add_label(self, color="#ff7b00", text="Название Рубрики"):
        text_lbl = tk.Label(master=self, bg=color, text=text)
        text_lbl.pack(fill=tk.X)

    def add_button(self, text="Конопка", command=None, pad_x=0, tip=None):
        button = tk.Button(master=self, text=text, relief=tk.FLAT, fg="#eee", bg="#454545", padx=pad_x, command=command)
        button.pack(pady=3)
        if tip:
            Hovertip(button, text=tip)

    def add_l_button(self, text="Конопка слева", command=None, padx=None):
        button = tk.Button(master=self, text=text, relief=tk.FLAT, fg="#eee", bg="#454545", command=command)
        button.pack(pady=3, padx=padx, side=tk.LEFT)

    def add_r_button(self, text="Конопка справа", command=None, padx=None):
        button = tk.Button(master=self, text=text, relief=tk.FLAT, fg="#eee", bg="#454545", command=command)
        button.pack(pady=3, padx=padx, side=tk.RIGHT)


class settings_window(child_window):
    def __init__(self, root):
        super().__init__(root)
        self.child_root.title('Настройки')
        self.child_root.geometry('250x380')
        self.to_parent_center(root)
        self.settings = config.read_all_config()
        self.main()
        self.child_root.focus_set()

    def show_log_widget(self):
        def get_check_deep_value():
            value = current_day_limit.get()
            if value == '-1' or value.isdigit():
                config.write("logs", "check_deep", f"{value}")
                text_lbl1.config(text=f"Глубина проверки лога - {value} заказов")
            day_entry.delete(0, tk.END)

        current_day_limit = tk.StringVar(self.child_root)
        text_lbl1 = tk.Label(self.child_root,
                             text=f"Глубина проверки лога - {self.settings['check_deep']} заказов", justify=tk.LEFT)
        text_lbl1.pack(anchor=tk.NW)
        entry_frame = tk.Frame(self.child_root)
        day_entry = tk.Entry(entry_frame, textvariable=current_day_limit, width=15)
        day_entry.pack(side=tk.LEFT, padx=3)
        change_button = tk.Button(entry_frame, relief=tk.FLAT, fg="#eee", bg="#454545", width=10,
                                  text="Задать", command=get_check_deep_value)
        change_button.pack(side=tk.RIGHT, padx=3)
        entry_frame.pack(anchor=tk.NW)

    def show_canvas(self):
        canv1 = tk.Canvas(self.child_root, width=250, height=1, bg="black")
        canv1.pack(pady=2)

    def show_image_stroke_size_widget(self):
        def stroke_size_change(val):
            config.write("IMAGE", "stroke_size", val)
            stroke_size_lbl1.config(text=f'Толщина обводки в пикселях: {val}')

        stroke_size_lbl1 = tk.Label(self.child_root)
        stroke_size_lbl1.pack(anchor=tk.NW)
        stroke_size_scale = tk.Scale(self.child_root, orient=tk.HORIZONTAL, from_=1, to=10, length=250, showvalue=False,
                                     command=stroke_size_change)
        stroke_size_scale.pack(anchor=tk.NW)
        stroke_size_scale.set(self.settings['stroke_size'])

    def show_image_gudeline_size_widget(self):
        def guideline_size_change(val):
            config.write("IMAGE", "guideline_size", val)
            guideline_size_lbl1.config(text=f'Толщина направляющих в пикселях: {val}')

        guideline_size_lbl1 = tk.Label(self.child_root)
        guideline_size_lbl1.pack(anchor=tk.NW)
        guideline_size_scale = tk.Scale(self.child_root, orient=tk.HORIZONTAL, from_=1, to=10, length=250,
                                        showvalue=False, command=guideline_size_change)
        guideline_size_scale.pack(anchor=tk.NW)
        guideline_size_scale.set(self.settings['guideline_size'])

    def show_color_chooser_widget(self):
        def init_stoke_color_change():
            color_inf = tkcc.askcolor()
            if not color_inf[1] is None:
                color = f"{color_inf[1]}"
                config.write("IMAGE", "stroke_color", color)
                current_stroke_color.config(bg=color)
            self.child_root.focus_set()

        def init_gl_color_change():
            color_inf = tkcc.askcolor()
            if not color_inf[1] is None:
                color = f"{color_inf[1]}"
                config.write("IMAGE", "guideline_color", color)
                current_guideline_color.config(bg=color)
            self.child_root.focus_set()

        color_chooser_frame = tk.Frame(self.child_root)
        stroke_color_lbl = tk.Label(color_chooser_frame, text='Цвет обводки')
        stroke_color_lbl.grid(row=0, column=0, padx=6)
        guideline_color_lbl = tk.Label(color_chooser_frame, text='Цвет направляющих')
        guideline_color_lbl.grid(row=0, column=1)
        current_stroke_color = tk.Button(color_chooser_frame, relief=tk.FLAT,
                                         bg=self.settings['stroke_color'], width=16, command=init_stoke_color_change)
        current_stroke_color.grid(row=1, column=0, padx=2)
        current_guideline_color = tk.Button(color_chooser_frame, relief=tk.FLAT,
                                            bg=self.settings['guideline_color'], width=16, command=init_gl_color_change)
        current_guideline_color.grid(row=1, column=1)
        color_chooser_frame.pack(anchor=tk.NW)

    def show_working_dir_frame(self):
        def change_pap(section):
            root_pap = tkfd.askdirectory(title="Выбор папки")
            if root_pap:
                config.write("working_dir", section, root_pap)
            if section == 'order_main_dir':
                order_dir_btn.config(text=f'{root_pap}')
            if section == 'fp_oper_disc':
                oper_disk_btn.config(text=f'{root_pap}')
            if section == 'roddom_main_dir':
                roddom_dir_btn.config(text=f'{root_pap}')
            self.child_root.focus_set()

        order_dir_lbl = tk.Label(self.child_root, text="Папка, куда сохраняются заказы:")
        order_dir_lbl.pack(anchor=tk.NW)
        order_dir_btn = tk.Button(self.child_root, width=34, relief=tk.FLAT, fg="#eee", bg="#454545", anchor='n',
                                  text=f'{self.settings["order_main_dir"]}',
                                  command=lambda: change_pap('order_main_dir'))
        order_dir_btn.pack(anchor=tk.NW, padx=2)
        oper_disk_lbl = tk.Label(self.child_root, text="Диск операторов фотопечати:")
        oper_disk_lbl.pack(anchor=tk.NW)
        oper_disk_btn = tk.Button(self.child_root, width=34, relief=tk.FLAT, fg="#eee", bg="#454545", anchor='n',
                                  text=f'{self.settings["fp_oper_disc"]}',
                                  command=lambda: change_pap('fp_oper_disc'))
        oper_disk_btn.pack(anchor=tk.NW, padx=2)
        roddom_dir_lbl = tk.Label(self.child_root, text="Папка загрузки заказов Роддома:")
        roddom_dir_lbl.pack(anchor=tk.NW)
        roddom_dir_btn = tk.Button(self.child_root, width=34, relief=tk.FLAT, fg="#eee", bg="#454545", anchor='n',
                                   text=f'{self.settings["roddom_main_dir"]}',
                                   command=lambda: change_pap('roddom_main_dir'))
        roddom_dir_btn.pack(anchor=tk.NW, padx=2)

    def close_btn(self):
        destroy_btn = tk.Button(self.child_root, text="Сохранить и выйти", relief=tk.FLAT, fg="#eee", bg="#454545",
                                command=self.child_root.destroy)
        destroy_btn.pack(side=tk.RIGHT, padx=2, pady=2)

    def main(self):
        self.show_log_widget()
        self.show_canvas()
        self.show_image_stroke_size_widget()
        self.show_image_gudeline_size_widget()
        self.show_color_chooser_widget()
        self.show_canvas()
        self.show_working_dir_frame()
        self.show_canvas()
        self.close_btn()
