from django.core.management.base import BaseCommand
from datetime import datetime
from apps.parser.models import Log
import json
import re

import time


class Command(BaseCommand):
    help = 'Парсит лог nginx'

    def add_arguments(self, parser):
        # Аргумент для приема информации о пути файла.
        parser.add_argument(
            'filepath',
            type=str,
            help='Абсолютный или относительный к management.py путь до файла лога'
        )
        # Аргумент для установки размера буфера чтения
        parser.add_argument(
            '-bs',
            '--buffersize',
            type=int,
            default=65536,
            help='Размер буфера чтения'
        )

    def handle(self, *args, **kwargs):
        filepath = kwargs.get('filepath', None)
        buffsize = kwargs.get('buffersize')

        if filepath is None or not filepath.endswith('.txt'):
            return
        # Читает часть лога в зависимости от размера буфера, парсит его и пишет в бд.
        with open(filepath, 'r', encoding='utf-8') as file:
            pre = ''
            while True:
                raw = file.read(buffsize)
                if not raw:
                    break
                data, suf = raw.rsplit('\n', 1)
                lst = self._json_parsing(pre + data)
                pre = suf
                Log.objects.bulk_create(lst)

    @staticmethod
    def _json_parsing(data: str):
        """Парсинг через преобразование в json коллекцию."""
        json_dcts = json.loads('[' + data.replace('\n', ',') + ']')
        for line in json_dcts:
            method, uri, *_ = line['request'].split(' ')
            yield Log(
                ip=line['remote_ip'], 
                date = datetime.strptime(line['time'], r'%d/%b/%Y:%H:%M:%S %z'), 
                method=method, 
                uri=uri, 
                status_code=line['response'], 
                content_length=line['bytes']
            )
