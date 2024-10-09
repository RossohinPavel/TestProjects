from django.urls import path
from .views import MailView


urlpatterns = [
    path('', MailView.as_view())
]
