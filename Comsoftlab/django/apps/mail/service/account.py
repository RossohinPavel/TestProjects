import email.message
from apps.mail.models import Account, Mail

# Либы для работы с почтой
import imaplib
import email

# Либы для парсинга
from email.header import decode_header
from datetime import datetime

# Типизация
from typing import Generator, Any


class IMAPAccaunt:
	"""Управление IMAP-аккаунтами"""

	YANDEX_SERVER = 'imap.yandex.ru'
	MAILRU_SERVER = ''
	GOOGLE_SERVER = ''

	@classmethod
	def from_queryset(cls, queryset) -> tuple:
		"""Получение объектов IMAPAccaunt из джанговской выборки"""
		return tuple(cls(a) for a in queryset)

	def __init__(self, account: Account):
		self._account = account
		self._imap = imaplib.IMAP4_SSL(self.server)
		self.raw_mails = []

	@property
	def server(self) -> str:
		"""Текущий imap-сервер исходя из адреса почты"""
		if '@yandex' in self._account.email:
			return self.YANDEX_SERVER
		if '@mail' in self._account.email:
			return self.MAILRU_SERVER
		if '@gmail' in self._account.email:
			return self.GOOGLE_SERVER

	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}: {self._account.email}>'

	def get_not_received_mails(self) -> Generator[int, Any, None]:
		"""Парсит почту на предмет неполученных сообщений. Обновляет атрибут self.raw_mails"""
		self._imap.login(self._account.email, self._account.password)
		_, folders = self._imap.list()
		for folder in folders:
			_, folder = folder.decode().rsplit(' ', 1)
			_, total_mails = self._imap.select(folder)
			for mail_num in range(int(total_mails[0]) + 1, 0, -1):
				_, raw_mail = self._imap.fetch(str(mail_num).encode(), '(RFC822)')
				if raw_mail[0] is None:
					continue
				mail = email.message_from_bytes(raw_mail[0][1])
				if self._account.mails.filter(mail_id=mail["Message-ID"]).exists():
					break
				self.raw_mails.append(mail)
				yield len(self.raw_mails)
		self._imap.logout()
	
	def parsing_mails(self) -> Generator[Mail, Any, None]:
		"""Парсит сообщения. Сохраняет информацию в базе данных и возвращает объект сообщения."""
		for mail in reversed(self.raw_mails):
			text, files = self.parse_content(mail)
			record = self._account.mails.create(
				mail_id=mail["Message-ID"],
    			subject=self.parse_subject(mail),
    			dispatch_date=self.parse_datetime(mail['Received'].split(', ')[-1]),
    			receive_date=self.parse_datetime(mail["Date"].split(', ')[-1][:-6]),
    			text=text,
    			files=files
			)
			yield record

	@staticmethod
	def parse_subject(mail) -> str:
		"""Парсит тему письма"""
		try:
			return decode_header(mail["Subject"])[0][0].decode()
		except:
			return '--theme--'

	@staticmethod
	def parse_datetime(date: str) -> datetime:
		"""Парсит дату и возвращает объект datetime"""
		return datetime.now()

	@staticmethod
	def parse_content(mail: email.message.Message) -> tuple[str, str | None]:
		"""
		Парсит содержимое письма. 
		Возвращает очищенный текст и список файлов
		"""
		return mail.get_content_maintype(), None
