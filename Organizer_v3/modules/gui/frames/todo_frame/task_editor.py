from ...source import *
from ...source import images
from .picker import DatetimePicker
from modules.trackers.task_tracker.task import Task


class TaskEditor(ChildWindow):
    """Создание и редактирование задачи."""
    width = 300
    height = 320
    win_title = 'Редактор задачи'

    def __init__(self, task: Task, /, **kwargs) -> None:
        # Объект задачи, с которым работает окно
        self._task = task

        # Основные виджеты. Ссылки на них нужны в функциях
        self.name: ttk.Entry
        self.description: ttk.Text
        self.datetime: DatetimePicker
        self.btn_execute: ttk.Button
        self.btn_redo: ttk.Button
        self.btn_save: ttk.Button

        super().__init__(**kwargs)
        self.bind('<Control-s>', self.cmd_save)
        self.bind('<<Save>>', self.cmd_save)
        self.after(50, lambda: self.event_generate('<Key-Tab>'))

    def main(self, **kwargs) -> None:
        self.draw_name_entry_widgets()
        self.draw_description_field()
        self.draw_date_and_time_picker()
        self.draw_buttons()
        self.configure_buttons()
    
    def draw_name_entry_widgets(self) -> None:
        """Отрисовка виджета имени задачи."""
        self.name = n = ttk.Entry(self, width=40)
        n.pack(padx=5, pady=(5, 0), fill=ttkc.X)
        n.insert(0, self._task.name)
    
    def draw_description_field(self) -> None:
        """Отрисовка текстового поля описания задачи."""
        self.description = txt = ttk.Text(self, width=1, height=1, wrap='word')
        txt.pack(padx=5, pady=(5, 0), fill=ttkc.BOTH, expand=1)
        d = self._task.description
        if d:
            txt.insert('1.0', d)
    
    def draw_date_and_time_picker(self) -> None:
        """Отрисовка виджета управления даты выполнения."""
        hl = HeaderLabel(self, text='Дата выполнения', anchor='n')
        hl.pack(padx=5, pady=(5, 0), fill=ttkc.X)

        self.datetime = dp = DatetimePicker(self, self._task.end)    #type: ignore
        dp.pack()
    
    def draw_buttons(self) -> None:
        """Отрисовка кнопок."""
        self.btn_execute = btn_execute = ttk.Button(
            self,
            style='success',
            padding=2,
            image=images.CHECK,
            command=self.cmd_execute,
        )
        btn_execute.pack(side=ttkc.LEFT, pady=5, padx=5)

        self.btn_redo = btn_redo = ttk.Button(
            self,
            style='primary',
            padding=2,
            image=images.REDO,
            command=self.cmd_redo,
        )
        btn_redo.pack(side=ttkc.LEFT, pady=5)

        delete = ttk.Button(
            self,
            style='danger',
            padding=2,
            image=images.DELETE,
            command=self.cmd_delete
        )
        delete.pack(side=ttkc.LEFT, pady=5, padx=5)

        cancel = ttk.Button(
            self,
            style='warning',
            text='Отмена',
            width=10,
            padding=2,
            command=self.destroy
        )
        cancel.pack(side=ttkc.RIGHT, padx=5, pady=5)

        self.btn_save = save = ttk.Button(
            self,
            style='success',
            text='Сохранить',
            width=10,
            padding=2,
            command=self.cmd_save,
        )
        save.pack(side=ttkc.RIGHT, pady=5)

    def configure_buttons(self) -> None:
        """Настраивает конфигурацию виджетов согласно тому, выполнена задача или нет."""
        exe = bool(self._task.execution)
        self.btn_execute.configure(state='disabled' if exe else 'normal')
        self.btn_redo.configure(state='normal' if exe else 'disabled')
        self.btn_save.configure(state='disabled' if exe else 'normal')
    
    def cmd_delete(self) -> None:
        """Удаление задачи."""
        self.destroy()
        self._task.delete()
    
    def cmd_execute(self) -> None:
        """Выполнение задачи"""
        self._task.execute()
        self.configure_buttons()
        
    def cmd_redo(self) -> None:
        """Возвращает задачу из выполненных в активные."""
        self._task.execution = None
        self._task.save()
        self.configure_buttons()

    def cmd_save(self, _ = None) -> None:
        """Обновляет значения в задаче и сохраняет их."""
        # Запрет на сохранение задачи, если она выполнена
        if self._task.execution: return

        self._task.name = self.name.get()
        self._task.description = self.description.get('1.0', ttkc.END)[:-1] or None
        self._task.end = self.datetime.get()

        self._task.save()
        self.destroy()
