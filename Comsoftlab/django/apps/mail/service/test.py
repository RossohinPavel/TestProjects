"""
Файл с различной тестовой писаниной
"""

import imaplib
import email
from sqlite3 import connect as sql_conn
from pathlib import Path



db_dir = Path(__file__).parent.parent.parent.parent


def main(acc: tuple[str]):
	mail = imaplib.IMAP4_SSL("imap.yandex.ru")
	res = mail.login(acc[0], acc[1])
	print(res)


if __name__ == '__main__':
	with sql_conn(db_dir / 'db.sqlite3') as conn:
		cursor = conn.cursor()
		cursor.execute(
			"""
			SELECT email, password
			FROM mail_account
			LIMIT 1
			"""
		)
		acc = cursor.fetchone()
		main(acc)
