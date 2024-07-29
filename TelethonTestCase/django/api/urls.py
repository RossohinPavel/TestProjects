from django.urls import path
from api import views
 
urlpatterns = [
    path('check/login', views.CheckAPIView.as_view(), name='check'),
    path('login', views.LoginAPIView.as_view(), name='login'),
    path('logout', views.LogoutAPIView.as_view(), name='logout'),
    path('messages', views.MessagesAPIView.as_view(), name='messages'),
    path('qr', views.get_qr, name='qr'),
    path('', views.WildberrysParserAPIView.as_view(), name='home')
]
