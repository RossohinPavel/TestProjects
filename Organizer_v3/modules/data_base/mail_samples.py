from .data_base import DataBase


class MailSamples(DataBase):
    """Предостовляет доступ для работы с базой данных текстовых шаблонов."""

    __slots__ = ()

    data_base = 'mail_samples.db'

    @DataBase.safe_connect
    def create(self, tag: str, name: str, text: str) -> None:
        """Сохранение нового текстового шаблона в бд"""
        self.cursor.execute(f'INSERT INTO Samples (name, tag, data) VALUES (?, ?, ?)', (name, tag, text))
        self.connect.commit()

    @DataBase.safe_connect
    def get_headers(self) -> list[tuple[str, str]]:
        """Получение заголовков текстовых шаблонов"""
        self.cursor.execute('SELECT tag, name FROM Samples')
        return self.cursor.fetchall()

    @DataBase.safe_connect
    def get(self, name: str) -> tuple[str, str, str]:
        """Получение тага, названия и текста шаблона"""
        self.cursor.execute('SELECT tag, name, data FROM Samples WHERE name=?', (name, ))
        return self.cursor.fetchone()

    @DataBase.safe_connect
    def delete(self, name: str) -> None: 
        """Удаление шаблона из хранилища"""
        self.cursor.execute('DELETE FROM Samples WHERE name=?', (name, ))
        self.connect.commit()
    
    @DataBase.safe_connect
    def update(self, old_name: str,  tag: str, name: str, text: str) -> None:
        """Обновление текстового шаблона в бд"""
        self.cursor.execute(f'UPDATE Samples SET name=?, tag=?, data=? WHERE name=?', (name, tag, text, old_name))
        self.connect.commit()
