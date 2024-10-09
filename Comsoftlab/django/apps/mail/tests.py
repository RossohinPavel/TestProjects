# Джанговские приблуды
from django.test import TestCase
# Модули моего приложения
from apps.mail.models import Account
# Либы для работы с почтой
import imaplib
import email
from email.header import decode_header
# Либы для декода контента почты
from bs4 import BeautifulSoup
import base64
import quopri


# Create your tests here.
class IMAPConnectionToYandexTestCase(TestCase):
	"""Различные тесты подключения"""

	@classmethod
	def setUpTestData(cls) -> None:
		"""Подготовка аккаута к тестированию"""
		cls.acc = cls.setup_test_accaunt()

	@staticmethod
	def setup_test_accaunt():
		"""Создает аккаунт по полученной из виртуального окружения инфы и возвращает его."""
		from os import getenv
		get_test_data = lambda: (getenv('TEST_EMAIL', None), getenv('TEST_PASS', None))
		email, password = get_test_data()
		if email is None:
			from dotenv import load_dotenv
			from django.conf import settings
			load_dotenv(settings.BASE_DIR.parent / '.env')
			email, password = get_test_data()
		acc = Account.objects.create(email=email, password=password)
		return acc
	

	def setUp(self) -> None:
		"""Задает подключение"""
		# Было бы логично залогиниться 1 раз в класметоде, но вылазит ошибка.
		# django не может сериализовать контекст объекта imaplib.IMAP4_SSL
		# В боевом режиме использовать imaplib.IMAP4_SSL вместе с with
		self.connection = imaplib.IMAP4_SSL("imap.yandex.ru")
		self.login_result = self.connection.login(self.acc.email, self.acc.password)


	def tearDown(self) -> None:
		"""Логаут из почты"""
		self.connection.logout()
		# self.connection.close()


	def test_connection(self):
		"""Тест подключения к почте"""
		# login_result - результат запроса, возвращаемое значение которого - кортеж из 2х элементов. 
		# 1й статус ответа ('OK' при успехе)
		# Второй - результат запроса. Это список из байтовых строк.
		self.assertEqual('OK', self.login_result[0])
		self.assertIsInstance(self.login_result[1], list)
		self.assertIsInstance(self.login_result[1][0], bytes)
		# Для перевода в обычную строку достаточно вызвать bytes.decode
		string = self.login_result[1][0].decode()
		self.assertIsInstance(string, str)
	

	def test_dir_list(self):
		"""Получение списка папок почты"""
		lst = self.connection.list()
		self.assertEqual('OK', lst[0])
		self.assertIsInstance(lst[1], list)
		# Для того, чтобы зайти в папку достаточно выделить из байтовой строки последнее слово.
		# Можно сделать это для 1 папки.
		byte_row = lst[-1][0].decode().split(' ')
		# Для того, чтобы получить письма нужно "зайти" в папку.
		# print(*lst[1], sep='\n')
		res = self.connection.select(byte_row[-1])
		self.assertEqual('OK', res[0])


	def test_get_inbox_mails_list(self):
		"""Получаем список писем из папки"""
		# Для получения писем нужно находится в определенной папке.
		# Такая абракадабра в иммени - из-за специфической кодировки.
		# Метод вернет количество писем в папке.
		res = self.connection.select("INBOX")
		self.assertEqual('OK', res[0])
		# Если выполнить поиск без каких-либо параметров, получим список номеров писем.
		res = self.connection.search(None, 'ALL')
		mails_nums = res[-1][0].split(b' ')
		# Метод для получения письма. При его использовании - письмо приобретет статус - прочитано.
		res, msg = self.connection.fetch(mails_nums[0], '(RFC822)')
		self.assertEqual('OK', res)
		

class EmailParsingTestCase(TestCase):
	"""Тестовые кейсы парсинга полученного письма."""

	@classmethod
	def setUpTestData(cls) -> None:
		"""Подготовка к тестированию"""
		acc = IMAPConnectionToYandexTestCase.setup_test_accaunt()
		connection = imaplib.IMAP4_SSL("imap.yandex.ru")
		connection.login(acc.email, acc.password)
		# Зайдем в папку и получим первое письмо 
		# (В тестовом случае папка - Госуслуги. Поменять на INBOX)
		# res, msg = connection.select("&BBMEPgRBBEMEQQQ7BEMEMwQ4-")
		res, msg = connection.select("INBOX")
		res, msg = connection.search(None, 'ALL')
		mails_nums = msg[0].split(b' ')
		res, msg = connection.fetch(mails_nums[-1], '(RFC822)')
		cls.raw_mail = msg[0]

	def test_get_mail_info(self):
		# self.raw_mail - В ответ получим кортеж байтов, в первом будет содержаться порядковый номер, стандарт и ещё какое-то число.
		# Извлекаем письмо при помощи метода message_from_bytes библиотеки email
		mail = email.message_from_bytes(self.raw_mail[1]) # Вернется объект типа email.message.Message
		# print(mail)
		# Некоторую информацию можно получить просто, некоторую нет.
		# Айди письма
		mail_id: str = mail["Message-ID"]
		# Тема письма
		# Тему письма нужно декодировать с исползованием метода decode_header, как и многую другую информацию.
		mail_subject: str = decode_header(mail["Subject"])[0][0].decode()
		# Дата отправки
		# Дата приходит в виде строки, дальше надо её парсить в формат datetime
		mail_dispatch_date = mail['Received'].split(', ')[-1]
		# Дата получения
		mail_receive_date = mail["Date"].split(', ')[-1][:-6]
		# e-mail отправителя
		mail_from = mail["Return-path"]				
		# Содержание (текст) письма
		# email результат может быть: 
		#  - простым текстовым сообщением, 
		#  - двоичным объектом, 
		#  - структурированной последовательностью подсообщений, каждое из которых имеет собственный набор заголовков и собственный payload.
		# Чтобы сразу разобраться с этим вопросом применяется метод .is_multipart(), 
		# который собственно и подсказывает, как дальше быть с письмом.
		if not mail.is_multipart():
			# В тестовом примере это несоставное письмо, с содержанием text\html
			mail_content = self.parse_mail_content(mail)
		else:
			# Чтобы продолжить нам нужно получить из объекта email.message.Message его полезную нагрузку, методом get_payload().
			# payload = mail.get_payload()
			mail_content = 'multipart'
		# Список файлов
		mail_files = self.walk_method_testing(mail)
		print(mail_id, mail_subject, mail_dispatch_date, mail_receive_date, mail_from, mail_content, mail_files, sep='\n')

	@staticmethod
	def parse_mail_content(mail):
		"""Парсит содержание письма в зависимости от его типа"""
		# Содержимое письма составное. Варианты: text/plain, text/html, application/pdf. Могут быть другие.
		mail_maintype = mail.get_content_maintype()
		# Если основное содержимое письма текст - то его нужно декодировать. Текст на родном никаким другим образом не получить.
		if mail_maintype == 'text':
			raw_content = EmailParsingTestCase.get_letter_decoded_content(mail)

		mail_subtype = mail.get_content_subtype()
		match mail_subtype:
			case 'html':
				res = BeautifulSoup(raw_content, 'lxml').get_text().replace('\r', '').replace('\n\n', '').replace('  ', '')

	@staticmethod
	def get_letter_decoded_content(letter):
		"""В зависимости от кодировки письма возвращает его содержание."""
		# all possible types: quoted-printable, base64, 7bit, 8bit, and binary
		match letter["Content-Transfer-Encoding"]:
			case "base64":
				encoding = letter.get_content_charset()
				return base64.b64decode(letter.get_payload()).decode(encoding)
			case "quoted-printable":
				encoding = letter.get_content_charset()
				return quopri.decodestring(letter.get_payload()).decode(encoding)
		return letter.get_payload()

	@staticmethod
	def walk_method_testing(mail):
		"""Тестирование метода walk"""
		for part in mail.walk():
			print(part.get_content_type())
			if part.get_content_disposition() == 'attachment':
				print('--', part.get_filename())
