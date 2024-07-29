from ..tracker import Tracker
from .task import Task
import modules.app_manager as APP


class TaskTracker(Tracker):
	"""Трекер для отслеживания и управления задачами в TODO фрейме."""

	__slots__ = ('tasks', )

	type Task = Task

	def __init__(self) -> None:
		self.tasks = Task.get_active_tasks()
		super().__init__()
	
	@APP.THREAD_MANAGER.parallel
	def __tasks_sort(self) -> None:
		"""Сортировка задач."""
		# Обновляем время в классе задач
		Task.now()

		# Обновляем статусы объектов задач
		for task in self.tasks:
			task.update_status()
		
		# Сортируем список. Приоритеты: выполнение, статус, дата окончания
		self.tasks.sort(key=lambda t: (bool(t.execution), t.status, t.end))

		# Вызываем перерисовку виджетов в todo фрейме
		APP.TODOFRAME.update_frame()
	
	auto_init = manual_init = __tasks_sort

	def add_task(self, task: Task) -> None:
		"""Добавление задачи в очередь отслеживания"""
		self.tasks.append(task)
	
	def delete_executed(self) -> None:
		"""Очищает очередь задач от выполненных"""
		ind = 0
		while ind < len(self.tasks):
			task = self.tasks[ind]
			if task.execution:
				del self.tasks[ind]
			else:
				ind += 1
		APP.TODOFRAME.update_frame()

	def delete_task(self, task_id: int) -> None:
		"""Удаляет задачу из очереди отслеживания и обновляет фрейм"""
		for i in range(len(self.tasks)):
			if self.tasks[i].id == task_id:
				del self.tasks[i]
				break
		APP.TODOFRAME.update_frame()
