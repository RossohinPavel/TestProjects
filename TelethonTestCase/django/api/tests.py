from django.test import TestCase
from django.urls import reverse
import os

# Create your tests here.
class EnviromentTestCase(TestCase):
    """Наличие переменных окружения."""

    def test_variables_exists(self):
        assert os.getenv('TG_API_ID') != None
        assert os.getenv('TG_API_HASH') != None
        # assert os.getenv('TEST_PHONE') != None


class WrongLoginTestCase(TestCase):
    """Реагирование на неправильный логин."""
    def setUp(self):
        self.login_path = reverse('login')

    def test_login1_wrong_get(self):
        # на метод GET
        response = self.client.get(self.login_path)
        json = response.json()
        assert response.status_code == 200
        assert 'error' in json

    def test_login1_wrong_post(self):
        # POST с некорректным номером
        response = self.client.post(self.login_path, data={'phone': '123456789'})
        json = response.json()
        assert response.status_code == 200
        assert 'error' in json
    
    def test_check_page(self):
        path = reverse('check')
        # впишем случайный подходящий номер
        response = self.client.get(path, QUERY_STRING=f'phone=89099091122')
        json = response.json()
        assert 'status' in json
        assert json['status'] == 'error'


class CorrectLoginTestCase(TestCase):
    """Логин с корректной информацией."""
    def setUp(self) -> None:
        self.test_phone = os.getenv('TEST_PHONE')
        path = reverse('login')
        self.response = self.client.post(path, {'phone': self.test_phone})
        self.json = self.response.json()
    
    def test_data(self):
        # Корректность возвращаемых данных
        assert self.response.status_code == 200
        assert 'qr_link_url' in self.json
        assert isinstance(self.json['qr_link_url'], str)
        assert self.json['qr_link_url'].endswith(f'qr?phone={self.test_phone}')
    
    def _get_check_request(self):
        path = reverse('check')
        response = self.client.get(path, QUERY_STRING=f'phone={self.test_phone}')
        return response.json()

    def test_login_logout(self):
        from .tclient import CLIENTS, LOOP
        # Создадим сессию с помощью номера телефона
        c = CLIENTS[self.test_phone]    # type: ignore
        c.start(self.test_phone)        # type: ignore

        # Ответ логинд
        assert self._get_check_request()['status'] == 'logined'

        # Сразу затестим логаут
        path = reverse('logout')
        response = self.client.post(path, {'phone': self.test_phone})
        assert response.json()['status'] == 'logout success'
        # Ответ на некорректный логаут
        response = self.client.post(path, {'phone': self.test_phone})
        assert 'error' in response.json()

    def test_qr(self):
        # Ожидание скана
        assert self._get_check_request()['status'] == 'waiting_qr_login'

        # Возврат страницы c qr
        link = self.json['qr_link_url']
        qr_response = self.client.get(link)
        assert qr_response.status_code == 200
        assert '<title>waiting_qr_login</title>' in str(qr_response.content)


class MessageHandlerTestCase(TestCase):
    """Обрабочик сообщений"""  
    def _login(self):
        self.test_phone = os.getenv('TEST_PHONE')
        self.test_user = 'me'
        self.response = self.client.post(reverse('login'), {'phone': self.test_phone})
        from .tclient import CLIENTS
        self.t_client = CLIENTS[self.test_phone]    # type: ignore
        self.t_client.start(self.test_phone)        # type: ignore
    
    def _logout(self):
        path = reverse('logout')
        self.client.post(path, {'phone': self.test_phone})
    
    def test_get_message(self):
        self._login()
        path = reverse('messages')
        # Проверим сразу с сохранением. в запросе save необязательный
        query = f'phone={self.test_phone}&uname={self.test_user}&save=True'
        response = self.client.get(path, QUERY_STRING=query)
        json = response.json()

        assert 'messages' in json
        messages = json['messages']
        # Тестирую на своих сообщениях. У меня всего 35 в сохраненных)
        assert len(messages) == 35
        # assert len(messages) == 50

        m0 = messages[0]
        assert 'username' in m0 and 'is_self' in m0 and 'message_text' in m0
        self._logout()

        assert self.test_user in os.listdir('Messages')
    
    def test_send_message(self):
        self._login()

        path = reverse('messages')
        msg = {"message_text": "привет!", "from_phone": self.test_phone, "username": self.test_user}
        response = self.client.post(path, msg)
        
        assert response.status_code == 200
        assert response.json()['status'] == 'ok'

        self._logout()


class WildberrysParserTestCase(TestCase):
    """Тест парсера wildberrys"""
    def test_request(self):
        path = reverse('home')
        response = self.client.post(path, {'wild': 'Носки'})
        json = response.json()
        assert len(json) == 10
