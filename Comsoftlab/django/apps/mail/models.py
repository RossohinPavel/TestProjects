from django.db import models

# Create your models here.
class Account(models.Model):
    """
    Модель для аккаунта почты.
    Вносить нужно данные для imap соединения.
    """
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Mail(models.Model):
    """Модель для хранения информации о письме."""
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='mails')
    mail_id = models.CharField(max_length=255)              # Уникальный идентификатор, который присваивает сам ящик
    subject = models.CharField(max_length=255)              # Тема письма
    dispatch_date = models.DateTimeField()                  # Дата отправки
    receive_date = models.DateTimeField()                   # Дата получения
    text = models.TextField()                               # Текстовое содержание письма
    files = models.CharField(max_length=255, null=True)     # "Список" файлов
