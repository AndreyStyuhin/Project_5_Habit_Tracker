from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Используем email как основной идентификатор.
    """
    username = models.CharField(max_length=150, unique=True, **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='Email')
    telegram_id = models.CharField(max_length=100, verbose_name='Telegram ID', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email