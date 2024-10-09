"""
Аналог views для channels части приложения
"""
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string

from .models import Account
from .service.account import IMAPAccaunt
from .templatetags.mail_tags import get_mail_row

from time import sleep
import json



class WSConsumer(WebsocketConsumer):
    """Обработка входящего асинхронного соединения из браузера"""

    def connect(self):
        self.accept()
        update = False
        self.send(json.dumps({'pb': {'message': 'Проверка сообщений'}}))
        imap_accounts = IMAPAccaunt.from_queryset(Account.objects.all())
        # Проверка сообщений
        for msg in self.check_mails(imap_accounts):
            update = True
            self.send(msg)
        # Добавление сообщений
        for msg in self.add_mails(imap_accounts):
            self.send(msg)
        self.send(json.dumps({'pb': {'message': 'Все сообщения  проверены'}}))
        if update:
            self.send(json.dumps({'update': True}))
        self.close()
    
    @staticmethod
    def check_mails(imap_accounts):
        """Генератор, который вызывает проверку сообщений"""
        for acc in imap_accounts:
            name = acc._account.email
            for count in acc.get_not_received_mails():
                msg = f'{name} писем прверено: {count}'
                yield json.dumps({'pb': {'message': msg}})
    
    @staticmethod
    def add_mails(imap_accounts: IMAPAccaunt):
        """Генератор, который вызывает добавление сообщений"""
        for acc in imap_accounts:
            mail_len = len(acc.raw_mails)
            msg = {
                'pb': {
                    'message': f'{acc._account.email} Добавление писем: ', 
                    'max': mail_len, 
                    'current': 0
                }
            }
            yield json.dumps(msg)
            msg['pb'].pop('max')
            for mail in acc.parsing_mails():
                msg['pb']['current'] += 1
                mail = render_to_string('mail_row.html', get_mail_row(mail))
                msg['mail'] = mail
                yield json.dumps(msg)
