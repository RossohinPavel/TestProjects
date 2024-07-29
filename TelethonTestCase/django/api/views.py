from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from api import tclient, wbparser


# Create your views here.
class PhoneCheckMixin(APIView):
    """Логика обработки ошибок"""
    @staticmethod
    def __check_phone(phone: str):
        if len(phone) != 11 or not phone.isdigit():
            raise ValueError('Incorrect number')

    def initial(self, request, *args, **kwargs):
        """Проверка корректности номера телефона в запросе"""
        if 'phone' in request.GET:
            self.__check_phone(request.GET['phone'])
        if 'phone' in request.POST:
            self.__check_phone(request.data['phone'])

        return super().initial(request, *args, **kwargs)
    
    def handle_exception(self, exc):
        """Обработка всех исключений"""
        return Response({'error': str(exc)})


class LoginAPIView(PhoneCheckMixin):
    """Авторизация пользователя."""
    def post(self, request):
        phone = request.data['phone']
        tclient.login(phone)
        return Response({'qr_link_url': request.build_absolute_uri(f'/qr?phone={phone}')})


class LogoutAPIView(PhoneCheckMixin):
    """Логаут"""
    def post(self, request):
        phone = request.data['phone']
        return Response({'status': tclient.logout(phone)})


class CheckAPIView(PhoneCheckMixin):
    def get(self, request):
        phone = request.GET['phone']
        return Response({'status': tclient.check(phone)})


def get_qr(request):
    """Представление для странички с qr"""
    if request.method == 'GET' and 'phone' in request.GET:
        status, token = tclient.get_token(request.GET['phone'])
        data = {'status': status, 'token': token}
        return render(request, 'api/qr.html', context=data)

    return HttpResponseNotFound()


class MessagesAPIView(PhoneCheckMixin):
    """Отправка сообщений"""
    def get(self, request):
        phone, uname = request.GET['phone'], request.GET['uname']
        save = request.GET.get('save', False)
        return Response({'messages': tclient.get_messages(phone, uname, save)})
    
    def post(self, request):
        data = request.data
        text, phone, username = data['message_text'], data['from_phone'], data['username']
        tclient.send_message(text, phone, username)
        return Response({'status': 'ok'})


class WildberrysParserAPIView(APIView):
    """Парсер wildberrys"""

    def post(self, request):
        if 'wild' in request.data:
            return Response(wbparser.parser(request.data['wild']))

        return HttpResponseNotFound()
