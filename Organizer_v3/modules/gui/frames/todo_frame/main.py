from ...source import *
from ...source import images
from .statistics import TODOStatWindow
from .task_interface import TaskInterface
from .task_editor import TaskEditor, Task
from .print_script import print_tasks


class TODOFrame(ScrolledFrame):
    """Фрейм для отображения списка задач. Он же TODO list."""

    def __init__(self, master: Any) -> None:
        super().__init__(
            master, 
            bootstyle='round', 
            padding=(0, 5, 0, 5)    #type: ignore
        )
        APP.TODOFRAME = APP.tdf = self
        self.draw_menu_button()
        master.bind('<Control-n>', self.create_task)
        master.bind('<<New>>', self.create_task)
    
    def draw_menu_button(self) -> None:
        """Отрисовка кнопки меню"""
        btn = ttk.Button(
            self.container,
            style='image.TButton',
            image=images.MENU,
            padding=5
        )
        btn.configure(command=self.draw_popup_menu(btn))
        btn.place(relx=0.88, rely=0.86)

    def draw_popup_menu(self, btn: ttk.Button):
        """Замыкание для отрисовки выпадающего меню."""
        match APP.OS_NAME:
            case 'nt': ix, iy = 116, 76
            case 'posix' | _: ix, iy = 85, 100

        menu = ttk.Menu(self.container, tearoff=0)

        menu.add_command(label='Добавить', accelerator='Ctrl+N', command=self.create_task)
        menu.add_separator()
        menu.add_command(label='Распечатать', command=self.print_tasks)
        menu.add_command(label='Статистика', command=lambda: TODOStatWindow())
        menu.add_separator()
        menu.add_command(label='Обновить', command=lambda: APP.TASK_TRACKER.manual_init())
        menu.add_command(label='Очистить', command=lambda: APP.TASK_TRACKER.delete_executed())          

        return lambda: menu.tk_popup(btn.winfo_rootx() - ix, btn.winfo_rooty() - iy)
    
    def update_frame(self) -> None:
        """Обновление виджета"""
        for children in self.winfo_children():
            children.destroy()
        
        badge = None

        for i, task in enumerate(APP.TASK_TRACKER.tasks):

            # Отрисовка виджетов задач
            ti = TaskInterface(self, task, name=f'ti_{i}')
            ti.pack(fill=ttkc.X, padx=(5, 12), pady=(0, 5))

            # Получение информации для метки кнопки
            if not badge:
                if task.execution:
                    continue
                if task.status < 0:
                    badge = 'danger'
                if task.status == 0:
                    badge = 'warning'

        if badge:
            APP.mw.todo.show_badge(badge)
        else:
            APP.mw.todo.hide_badge()

    def create_task(self, _e: tkinter.Event | None = None) -> None:
        """Создание новой задачи."""
        # Дополнительно переключаем на виджет с задачами
        APP.MAIN_WINDOW.todo.click(None)
        TaskEditor(Task.new())
    
    def print_tasks(self) -> None:
        """Комманда на распечатывание задач."""
        lst = [t.text for t in APP.TASK_TRACKER.tasks]
        print_tasks(lst)
