from .data_base import DataBase
from typing import Literal


class TasksDB(DataBase):
	"""Работа с базой данных задач."""

	__slots__ = ()
	data_base = 'tasks.db'

	@DataBase.safe_connect
	def delete(self, id: int) -> None:
		"""Удаление задачи"""
		self.cursor.execute('DELETE FROM Tasks WHERE id=?', (id, ))
		self.connect.commit()

	@DataBase.safe_connect
	def get_tasks(self, mode: Literal['active', 'all'] = 'active') -> list[tuple]:
		"""Возвращает указанные задачи"""
		req = ' WHERE execution IS NULL' if mode =='active' else ''
		self.cursor.execute('SELECT * FROM Tasks' + req)
		return self.cursor.fetchall()
	
	@DataBase.safe_connect
	def update(
		self, 
		id: int, 
		name: str, 
		descr: str | None, 
		creation: str, 
		end: str, 
		execution: str | None
		) -> int:
		"""Обновляет базу данных. Возвращает id записи."""

		if id == 0:
			self.cursor.execute('INSERT INTO Tasks (name) VALUES (0)')
			self.cursor.execute('SELECT seq FROM sqlite_sequence WHERE name=? LIMIT 1', ('Tasks', ))
			id = self.cursor.fetchone()[0]

		self.cursor.execute(
			"""
				UPDATE Tasks
				SET name=?, description=?, creation=?, end=?, execution=?
				WHERE id=?
			""",
			(name, descr, creation, end, execution, id)
		)
		self.connect.commit()
		return id
