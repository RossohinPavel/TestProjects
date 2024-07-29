from datetime import datetime, timedelta
from modules import app_manager as APP
from ...data_base import TasksDB
from typing import Self


_TasksDB = TasksDB()


class Task:
    """Интерфейс управления задачей."""

    __slots__ = ('id', 'name', 'description', 'creation', 'end', 'execution', 'status')

    _now = datetime.now()
    _dt_pattern = r'%Y-%m-%d %H:%M'

    def __init__(
        self, 
        id: int, 
        name: str, 
        description: str | None, 
        creation: datetime | str,
        end: datetime | str,
        execution: datetime | str | None
    ):
        self.id = id                                    # id задачи. Присваивается sqlite базой данных.
        self.name = name                                # Имя задачи
        self.description = description                  # Описание задачи
        self.creation = self._convert(creation)         # Дата создания задачи
        self.end = self._convert(end)                   # Планируемая дата окончания задачи. Дедлайн
        self.execution = self._convert(execution)       # Дата выполнения задачи

        # Вспомогательная переменная status. 
        # - Отрицательные значения - задача просрочена
        # 0 - задача актуальна. Срок исполнения меньше суток. 
        # 1 и больше - Задача актуальна. Срок исполнения больше суток
        self.status = 0

    @classmethod
    def _convert(cls, date_string: datetime | str | None) -> datetime | None:
        """Конвертирует строку в объект datetime по шаблону %Y-%m-%d %H:%M."""
        if isinstance(date_string, str):
            return datetime.strptime(date_string, cls._dt_pattern)

        return date_string
    
    @classmethod
    def get_active_tasks(cls) -> list[Self]:
        """Возвращает невыполненные задачи"""
        tasks = _TasksDB.get_tasks()
        for i, v in enumerate(tasks):
            tasks[i] = cls(*v)      #type: ignore

        return tasks                #type: ignore

    @classmethod
    def new(cls, _name='#Новая задача') -> Self:
        """Создание новой задачи."""
        now = cls.now()
        return cls(0, _name, None, now, now + timedelta(days=1), None)
    
    @classmethod
    def now(cls) -> datetime:
        """Обновляет время в классе и возвращает объект datetime."""
        cls._now = datetime.now()
        return cls._now
    
    def delete(self):
        """Удаляет задачу из базы данных и отслеживающего трекера"""
        APP.TASK_TRACKER.delete_task(self.id)
        _TasksDB.delete(self.id)
    
    def execute(self) -> None:
        """Выполняет задачу. В поле execution записывается текущее значение времени"""
        self.execution = datetime.now()
        self.save()
    
    def __str__(self) -> str:
        name = self.name

        descr = self.description or ''

        status = 'Статус: '
        if self.execution:
            status += 'Выполнена'
        else:
            if self.status < 0:
                status += 'Просрочена'
            if self.status == 0:
                status += 'Приоритетное выполнение'
            if self.status > 0:
                status += 'Ожидает выполнения'
  
        create = f'Создана: {self.creation.strftime(self._dt_pattern)}'
        end = f'Закончить к: {self.end.strftime(self._dt_pattern)}'
        execution = ''
        if self.execution:
            execution = f'Выполнена: {self.execution.strftime(self._dt_pattern)}'

        sep = '-' * len(max((name, create, status, end, execution), key=len))

        return '\n'.join(x for x in (name, descr, sep, status, create, end, execution) if x)


    def update_status(self) -> None:
        """Обновляет статус задачи."""
        delta = self.end - self._now    #type: ignore
        self.status = delta.days

    def save(self) -> None:
        """Сохраняет задачу. Вызывает обновление трекера"""
        # Добавляем новую задачу в трекер
        if self.id == 0:
            APP.TASK_TRACKER.add_task(self)

        # Преобразуем атрибуты времени в строки
        crе = self.creation.strftime(self._dt_pattern)          #type: ignore
        end = self.end.strftime(self._dt_pattern)               #type: ignore
        exe = self.execution
        if exe:
            exe = exe.strftime(self._dt_pattern)                #type: ignore
        
        # Сохраняем / обновляем задачу
        self.id = _TasksDB.update(self.id, self.name, self.description, crе, end, exe)

        # Обновляем трекер
        APP.TASK_TRACKER.manual_init()
    
    @property
    def text(self) -> str:
        """Возвращает печатную форму задачи."""
        # string = '   \u20de ' + '\u035f'.join(self.name) + '\n'
        string = '   \u20de ' + self.name
        string += '\n\tВыполнить к: ' + self.end.strftime(self._dt_pattern)     #type: ignore
        if self.description:
            string += '\n\tОписание: ' + self.description
        string += '\n'
        return string
