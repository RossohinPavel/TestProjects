import json
import os

from django.test import TestCase
from apps.parser.management.commands.parse import Command
from apps.parser.models import Log

TEST_ROWS = [
    {"time": "17/May/2015:08:05:32 +0000", "remote_ip": "93.180.71.3", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"},
    {"time": "17/May/2015:08:05:23 +0000", "remote_ip": "93.180.71.3", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"},
    {"time": "17/May/2015:08:05:24 +0000", "remote_ip": "80.91.33.133", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.17)"},
    {"time": "17/May/2015:08:05:34 +0000", "remote_ip": "217.168.17.5", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 200, "bytes": 490, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.10.3)"},
    {"time": "17/May/2015:08:05:09 +0000", "remote_ip": "217.168.17.5", "remote_user": "-", "request": "GET /downloads/product_2 HTTP/1.1", "response": 200, "bytes": 490, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.10.3)"},
    {"time": "17/May/2015:08:05:57 +0000", "remote_ip": "93.180.71.3", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"},
    {"time": "17/May/2015:08:05:02 +0000", "remote_ip": "217.168.17.5", "remote_user": "-", "request": "GET /downloads/product_2 HTTP/1.1", "response": 404, "bytes": 337, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.10.3)"},
    {"time": "17/May/2015:08:05:42 +0000", "remote_ip": "217.168.17.5", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 404, "bytes": 332, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.10.3)"},
    {"time": "17/May/2015:08:05:01 +0000", "remote_ip": "80.91.33.133", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.17)"},
    {"time": "17/May/2015:08:05:27 +0000", "remote_ip": "93.180.71.3", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"},
]

# Create your tests here.
class CommandsTestCase(TestCase):
    cmd = Command()

    @classmethod
    def setUpClass(cls):
        """Имитируем наличие лог-файла"""
        super().setUpClass()
        with open('test.txt', 'w', encoding='utf-8') as file:
            for line in TEST_ROWS:
                raw = json.dumps(line) + '\n'
                file.write(raw)

    @classmethod
    def tearDownClass(cls):
        """После проверки - затрем тестовый файл"""
        os.remove('test.txt')
        super().tearDownClass()

    def test_command(self):
        """Отработка функции и корректность данных в базе"""
        self.cmd.handle(filepath='test.txt', buffsize=1024)
        logs = Log.objects.all().order_by('id')
        assert len(logs) == 10
        for i, log in enumerate(logs):
            test_row = TEST_ROWS[i]
            assert log.ip == test_row['remote_ip']
            assert log.date.strftime(r'%d/%b/%Y:%H:%M:%S %z') == test_row['time']
            assert log.method + ' ' + log.uri == test_row['request'][:-9]
            assert log.status_code == test_row['response']
            assert log.content_length == test_row['bytes']
