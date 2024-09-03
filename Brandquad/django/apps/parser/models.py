from django.db import models

# Create your models here.
class Log(models.Model):
    """Представление лог файла"""

    ip = models.GenericIPAddressField()
    date = models.DateTimeField()
    method = models.CharField(max_length=10)
    uri = models.URLField()
    status_code = models.PositiveSmallIntegerField()
    content_length = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.date} - {self.ip}'