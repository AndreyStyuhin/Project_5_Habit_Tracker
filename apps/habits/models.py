from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    """
    Модель Привычки.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=200, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=500, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Связанная привычка',
        **NULLABLE
    )
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=200, verbose_name='Вознаграждение', **NULLABLE)
    duration = models.PositiveSmallIntegerField(verbose_name='Время на выполнение (в секундах)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    last_sent_time = models.DateTimeField(verbose_name='Время последней отправки', **NULLABLE)

    def __str__(self):
        return f'{self.action} в {self.time} ({self.place})'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('time',)