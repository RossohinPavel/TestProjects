import tkinter as tk


root = tk.Tk()

LISTBOX_VARS = {}


class AssistWindow(tk.Toplevel):
    """Вспомогательное окно для занесения информации"""
    def __init__(self, parent_root, cell):
        super().__init__(master=parent_root)
        self.cell = cell
        self.order_name = tk.StringVar()
        self.book_qty = tk.StringVar()
        self.pages_qty = tk.StringVar()
        self.__main()
        
    def __main(self):
        self.config(border=1, relief='solid')
        self.show_order_entry_frame()
        self.show_quantity_frame(0, 'Количество', self.book_qty, 'Добавить', self.add_func)
        self.show_quantity_frame(2, 'Развороты', self.pages_qty, 'Отмена', self.destroy)
        self.to_desctop_center()
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def to_desctop_center(self):
        self.update_idletasks()
        parent_width = root.winfo_width()
        parent_height = root.winfo_height()
        parent_place_x = root.winfo_x()  
        parent_place_y = root.winfo_y()
        child_width = self.winfo_width()
        child_height = self.winfo_height()
        place_x = ((parent_width - child_width) // 2) + parent_place_x + 10
        place_y = ((parent_height - child_height) // 2) + parent_place_y - 100
        self.geometry(f"+{place_x}+{place_y}")

    def show_order_entry_frame(self):
        lbl1 = tk.Label(self, text='Введите номер заказа')
        lbl1.grid(row=0, column=0, columnspan=3)
        entry1 = tk.Entry(self, font='Arial 20', width=14, textvariable=self.order_name)
        entry1.grid(row=1, column=0, columnspan=3)

    def show_quantity_frame(self, column, lbl_txt, entry_var, btn_txt, btn_fx):
        lbl = tk.Label(self, text=lbl_txt)
        lbl.grid(row=2, column=column)
        entry = tk.Entry(self, font='Arial 20', width=6, textvariable=entry_var)
        entry.grid(row=3, column=column, sticky='ew')
        if column == 0:
            separator = tk.Label(self, text='/')
            separator.grid(row=3, column=1)
        add_btn = tk.Button(self, text=btn_txt, command=btn_fx, font='Arial 14')
        add_btn.grid(row=4, column=column, sticky='ew')
        
    def add_func(self):
        order_name, book_qty, page_qty = self.order_name.get(), self.book_qty.get(), self.pages_qty.get()
        if not order_name or not book_qty or not page_qty:
            return
        string = f'{order_name} - {book_qty}/{page_qty}'
        LISTBOX_VARS[self.cell].insert(0, string)
        self.comparison_func()
        self.destroy()

    @staticmethod
    def comparison_func():
        left_box = LISTBOX_VARS['Обложки'].get(0, LISTBOX_VARS['Обложки'].size())
        right_box = LISTBOX_VARS['Развороты'].get(0, LISTBOX_VARS['Развороты'].size())
        comp = set(left_box) & set(right_box)
        if comp:
            LISTBOX_VARS['result'].insert(0, *comp)
            LISTBOX_VARS['Обложки'].delete(left_box.index(*comp))
            LISTBOX_VARS['Развороты'].delete(right_box.index(*comp))


class WorkFrame:
    """Объект для хранения информации о парных виджетов и функции работы с ними"""
    def __init__(self, lbl, side):
        self.lbl = lbl
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=1, fill=tk.BOTH, side=side)

    def show_work_frame(self):
        label = tk.Label(self.main_frame, text=self.lbl)
        label.pack(expand=1, fill=tk.X)
        button_frame = tk.Frame(self.main_frame)
        plus_button = tk.Button(button_frame, text='+', width=4, font='arial 12 bold', command=self.plus_func)
        plus_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        minus_button = tk.Button(button_frame, text='–', width=4, font='arial 12 bold', command=self.minus_func)
        minus_button.pack(side=tk.RIGHT, expand=1, fill=tk.X)
        button_frame.pack(expand=1, fill=tk.X)
        frame = tk.Frame(self.main_frame)
        list_box = tk.Listbox(frame, height=25)
        LISTBOX_VARS[self.lbl] = list_box
        list_box.pack(expand=1, fill=tk.BOTH, side=tk.LEFT)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=list_box.yview)
        scrollbar.pack(fill='y', side=tk.RIGHT)
        list_box["yscrollcommand"] = scrollbar.set
        frame.pack(expand=1, fill=tk.BOTH)

    def plus_func(self):
        AssistWindow(root, self.lbl)
        
    def minus_func(self):
        elem_ind = LISTBOX_VARS[self.lbl].curselection()
        if elem_ind:
            LISTBOX_VARS[self.lbl].delete(*elem_ind)


def minus_btn():
    elem_ind = LISTBOX_VARS['result'].curselection()
    if elem_ind:
        LISTBOX_VARS['result'].delete(*elem_ind)


def show_result_frame():
    frame = tk.Frame(root)
    result_listbox = tk.Listbox(frame)
    LISTBOX_VARS['result'] = result_listbox
    result_listbox.pack(expand=1, fill=tk.BOTH, side=tk.LEFT)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=result_listbox.yview)
    scrollbar.pack(fill='y', side=tk.RIGHT)
    result_listbox["yscrollcommand"] = scrollbar.set
    frame.pack(expand=1, fill=tk.BOTH)
    minus_button = tk.Button(root, text='–', width=4, font='arial 12 bold', command=minus_btn)
    minus_button.pack(anchor=tk.E)


if __name__ == '__main__':
    show_result_frame()
    left = WorkFrame('Обложки', tk.LEFT)
    right = WorkFrame('Развороты', tk.RIGHT)
    left.show_work_frame()
    right.show_work_frame()
    root.mainloop()
