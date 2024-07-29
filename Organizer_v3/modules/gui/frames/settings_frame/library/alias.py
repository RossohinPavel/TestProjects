from ....source import *
from ....source import images
from tkinter import Listbox


class AliasInterface:
    """Класс отрисовки виджетов и управления псевдонимами"""

    __slots__ = ('listbox', )

    def __init__(self, master: ttk.Frame) -> None:
        #Листбокс
        self.listbox = Listbox(master)
        self.listbox.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1)

        # Прокрутка листбокса
        sb = ttk.Scrollbar(
            master, 
            style='round',
            orient='vertical', 
            command=self.listbox.yview
        )
        sb.pack(side=ttkc.LEFT, fill=ttkc.Y)
        self.listbox.configure(yscrollcommand=sb.set)

        add_btn = ttk.Button(
            master,
            style='success',
            padding=1,
            image=images.PLUS,
            command=self.add_command
        )
        add_btn.place(relx=0.835, rely=0.910)

        del_btn = ttk.Button(
            master,
            style='danger',
            padding=1,
            image=images.DELETE, 
            command=self.delete_command
        )
        del_btn.place(relx=0.9, rely=0.910)


    def add_command(self) -> None:
        """Добавление значения в Listbox по нажатию конопки."""
        pos = self.listbox.winfo_rootx() + 75, self.listbox.winfo_rooty() - 40

        # Оборачиваем в try, чтобы не кидало ошибку при закрытом дочернем окне.
        try:
            res = Querybox.get_string(
                prompt='Введите название псевдонима',
                title='Добавление псевдонима',
                parent=self.listbox,
                position=pos
            )
            if self.listbox.winfo_viewable() and res:
                self.insert(res)
        except: pass

    def clear(self) -> None:
        """Очищает все элементы листбокса"""
        self.listbox.delete(0, ttkc.END)

    def delete_command(self) -> None:
        """Удаляет элемент по выбранному индексу"""
        try: self.listbox.delete(self.listbox.curselection())
        except: pass
    
    def get(self) -> tuple[str]:
        """Получение списка псевдонимов"""
        return self.listbox.get(0, ttkc.END)
    
    def insert(self, *args) -> None:
        """Вставка значения в Listbox с проверкой на дубликаты"""
        elements = self.listbox.get(0, ttkc.END)
        for value in args:
            if value not in elements:
                self.listbox.insert(ttkc.END, value)
