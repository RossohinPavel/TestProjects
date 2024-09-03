from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Course

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='balance'
    )
    value = models.PositiveIntegerField(
        default=1000
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)
    
    def __str__(self) -> str:
        return f'Balance={self.value}'


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
