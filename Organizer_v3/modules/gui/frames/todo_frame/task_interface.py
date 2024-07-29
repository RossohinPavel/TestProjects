from ...source import *
from ttkbootstrap.tooltip import ToolTip
from .task_editor import TaskEditor
from modules.trackers.task_tracker.task import Task


class TaskInterface(ttk.Frame):
    """Интерфейс для работы с задачей."""

    def __init__(self, master: Any, task: Task, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._task = task
        self._var = ttk.IntVar(self, value=1 if task.execution else 0)
        self.draw_execute_btn()
        self.draw_task_btn()
    
    def draw_execute_btn(self) -> None:
        """Отрисовка кнопки выполнения задачи."""
        frame = ttk.Frame(self, width=18, height=15)
        frame.pack(side=ttkc.LEFT)

        btn = ttk.Checkbutton(
            self,
            padding=1,
            style='success',
            variable=self._var,
            command=self._task.execute
        )
        btn.place(x=0, y=4)

        if self._var.get():
            btn.configure(state='disabled')
    
    def draw_task_btn(self) -> None:
        """Отрисовка кнопки задачи"""
        btn = ttk.Button(
            self, 
            padding=(1, 2, 2, 2), 
            style=self.__get_task_status(),
            command=lambda: TaskEditor(self._task)
        )
        btn.pack(side=ttkc.RIGHT, fill=ttkc.X, expand=1)
        text = self._task.name
        
        # Если задача выполнена, текст на фрейме зачеркивается
        btn.configure(text=text)
        ToolTip(btn, text=str(self._task), delay=1000)
        
    def __get_task_status(self) -> str:
        """Возвращает стиль фрейма, согласно статусу задачи"""
        # Для выполненных задач - приглушенный стиль.
        if self._task.execution:
            return 'ljf.secondary.Link.TButton'
        
        # Стиль с желтым подчеркиванием для задач, 
        # время которых на выполнение осталось меньше дня
        if self._task.status == 0:
            return 'ljf.warning.TButton'
        
        # Красное подчеркивание для просроченных задач
        if self._task.status < 0:
            return 'ljf.danger.TButton'
        
        # Обычный стиль для задач, время выполнения которых больше дня
        return 'ljf.Link.TButton'
