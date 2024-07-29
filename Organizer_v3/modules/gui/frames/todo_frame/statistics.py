from ...source import *
from modules.data_base.tasks import TasksDB
from modules import app_manager as APP
from datetime import datetime
from functools import lru_cache


DATABASE = TasksDB()


class TODOStatWindow(ChildWindow):
    """Окно вывода статистики для TODO фрейма"""
    width, height = 550, 350
    win_title = 'Статистика'

    def __init__(self, master: Any = None, /, **kwargs) -> None:
        self.table = ttk.Treeview
        self.now_date = datetime.now().strftime(r'%Y-%m-%d %H:%M')
        super().__init__(master, **kwargs)

    def main(self, **kwargs) -> None:
        self.show_table_widgets()
        self.update_table()
    
    def show_table_widgets(self) -> None:
        """Отрисовка и настройка внешнего вида таблицы"""
        columns = ('period', 'created', 'done', 'overdue', 'rate')
        columns_r = ('Период', 'Создано', 'Выполнено', 'Просроченно', 'Успешность')
        columns_width = (80, 40, 40, 40, 40)
        self.table = ttk.Treeview(self, show='headings', columns=columns)
        
        for i, column in enumerate(columns):
            self.table.heading(column, text=columns_r[i], anchor=ttkc.W)
            self.table.column(column=i, stretch=ttkc.YES, width=columns_width[i],)

        self.table.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1)

        scroll = ttk.Scrollbar(
            self, 
            orient='vertical', 
            style='round',
            command=self.table.yview
            )
        scroll.pack(side=ttkc.LEFT, fill=ttkc.Y)
        self.table.configure(yscrollcommand=scroll.set)

    @APP.THREAD_MANAGER.parallel
    def update_table(self) -> None:
        """Обновляет таблицу данными из базы данных"""
        self.get_row_from_date(self.now_date[0:10])
        tasks = DATABASE.get_tasks('all')
        tasks.reverse()

        for task in tasks:
            self._identify_creatin_date(task)       #type: ignore
            self._identify_execution_date(task)     #type: ignore
            self._identify_overdue_status(task)     #type: ignore
        
        self._identify_success_rate()

    @lru_cache
    def get_row_from_date(self, date_str: str) -> str:
        """
            Возвращает индекс строки из table по переданной дате.
            Если такой строки нет, то создается новая строка.
        """
        if self.get_row_from_date.cache_info().currsize == 127:
            self.get_row_from_date.cache_clear()
        
        index = None

        for item_index in self.table.get_children(''):              #type: ignore
            mon, sun = self.table.item(item_index)['tags']     #type: ignore 
            if sun >= date_str >= mon:
                index = item_index
                break
        
        if index is None:
            date = datetime.strptime(date_str, r'%Y-%m-%d').isocalendar()
            sunday = datetime.fromisocalendar(date.year, date.week, 7)
            monday = datetime.fromisocalendar(date.year, date.week, 1)

            val = (f'{monday.strftime(r'%d.%m.%y')} - {sunday.strftime(r'%d.%m.%y')}', 0, 0, 0, 100)
            
            index = self.table.insert(
                '', 
                ttkc.END,
                values=val,
                tags=[monday.strftime(r'%Y-%m-%d'), sunday.strftime(r'%Y-%m-%d')]
                )   #type: ignore

        return index

    def _identify_creatin_date(self, task: tuple[str, ...]) -> None:
        """Определяет дату создания задачи и обновляет значение в соответствующей ячейке"""
        item_index = self.get_row_from_date(task[3][:10])
        values = self.table.item(item_index)['values']                  #type: ignore                                     #type: ignore
        self.table.set(item=item_index, column=1, value=values[1] + 1)  #type: ignore

    def _identify_execution_date(self, task: tuple[str, ...]) -> None:
        """Определяет дату выполнения задачи и обновляет значение в соответствующей ячейке"""
        if task[-1]:
            item_index = self.get_row_from_date(task[-1][:10])
            values = self.table.item(item_index)['values']                  #type: ignore                                     #type: ignore
            self.table.set(item=item_index, column=2, value=values[2] + 1)  #type: ignore
    
    def _identify_overdue_status(self, task: tuple[str, ...]) -> None:
        """Определяет, что задача просрочена и обновляет значение в соответствующей ячейке """
        date = self.now_date if task[-1] is None else task[-1]
        
        if date > task[-2]:
            item_index = self.get_row_from_date(task[4][:10])
            values = self.table.item(item_index)['values']                  #type: ignore                                     #type: ignore
            self.table.set(item=item_index, column=3, value=values[3] + 1)  #type: ignore
    
    def _identify_success_rate(self) -> None:
        """Определяет рейтинг успешности"""
        for item_index in self.table.get_children(''):                  #type: ignore
            values = self.table.item(item_index)['values']              #type: ignore
            if values[-3]:
                percent = round(100 - (values[-2] / values[-3] * 100), 2)   #type: ignore
                self.table.set(item=item_index, column=4, value=percent)    #type: ignore
