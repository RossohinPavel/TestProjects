from ....source import *
from .alias import AliasInterface
from . import tabs


class AssistWindow(ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    width = 400
    height = 360

    def __init__(self, master: Any, product_name: str) -> None:
        # Сохраняем значения в объекте
        product = APP.lib.by_name(product_name)
        self._product_name = product.name 
        self._product = product._asdict()
        self._vars = {}
        self._alias: AliasInterface = None  #type: ignore
        self._update_func = master.redraw

        # Вызываем базовый класс
        super().__init__(master)
    
    def __update_title(self) -> None:
        """Обновляет заголовок окна"""
        self.title(f'Редактирование {self._product['name']}')  #type: ignore
    
    def main(self, **kwargs) -> None:
        self.__update_title()

        # Рисуем Notebook
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=1, padx=5, pady=5)

        nb.add(tabs.CommonTab(nb, self), text='Общее')
        self.draw_aliases_tab(nb)
        nb.add(tabs.CoverTab(nb, self), text='Обложка')
        nb.add(tabs.BlockTab(nb, self), text='Блок')

        # Кнопка сохранить
        ttk.Button(
            self, 
            style='success',
            padding=2,
            text='Сохранить', 
            width=14, 
            command=self.write_to_library
        ).pack(pady=(0, 5))
    
    def cmd_copy_product(self) -> None:
        """Копирование продукта"""
        new_name =  self._product['name'] + ' копия'
        self._product['name'] = new_name
        self._vars['name'].set(new_name)
        self.__update_title()
        self._product_name = new_name
        values = tuple(self._product.values())[1:]
        self._alias.clear()
        self.master.cmd_add_product((new_name, *values))
        msg = f'Создан новый продукт\n{new_name}'
        tkmb.showinfo('Копирование продукта', msg, parent=self)

    def cmd_delete_product(self) -> None:
        """Удаление продукта из библиотеки"""
        msg = f'Вы точно хотите удалить\n{self._product_name}?'
        if tkmb.askyesno('Удалиние продукта', msg, parent=self):
            APP.lib.delete(self._product_name)
            self.destroy()
            self._update_func()
    
    def draw_aliases_tab(self, notebook: ttk.Notebook) -> None:
        """Отрисовка вкладки под псевдонимы продуктов."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Псевдонимы')
        self._alias = AliasInterface(frame)
        aliases = (x[0] for x in APP.lib.get_aliases(self._product['name']))
        self._alias.insert(*aliases)

    def get_values_from_widgets(self):
        """
            Метод для получения информации из виджетов.\n
            Обновляет словарь _product, если все значения заполнены\n
            генерирует исключение в противном случае.
        """
        # Целочисленные значения для отдельной проверки
        numbered_var = (
            'carton_length', 'carton_height', 'cover_flap', 'cover_joint', 
            'dc_top_indent', 'dc_left_indent', 'dc_overlap'
        )
        for key, var in self._vars.items():
            # Получаем значение
            if var is not None:
                var = var.get()

            # Генерируем исключение, если поле пустое
            if var == '': 
                raise Exception(f'Нет данных в поле: {key}')
            
            # Генерируем исключение для вводимых полей с числами, если там есть буквы
            if var and key in numbered_var:
                if not var.isdigit():
                    raise Exception(f'Проверьте поле: {key}')

            self._product[key] = var

    def write_to_library(self) -> None:
        """Ф-я для обновления/записи информации библиотеку"""
        # Обработчик исключений, чтобы прервать логику выполнения в случае ошибки
        try:
            # Получаем продукт и псевдонимы
            self.get_values_from_widgets()
            aliases = self._alias.get()

            # Обновляем продукт
            APP.lib.change(self._product_name, self._product, aliases)

            # Обновляем виджеты в основном окне
            self._product_name = self._product['name']
            self.__update_title()
            self._update_func()

            # Вывод сообщения об успехе операции
            tkmb.showinfo('Редактирование', f'Данные обновлены для:\n{self._product_name}', parent=self)
        
        # Вывод сообщения об ошибке
        except Exception as e: 
            tkmb.showwarning('Ошибка', str(e), parent=self)
