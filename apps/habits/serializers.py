from rest_framework import serializers
from .models import Habit
from .validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Привычки.
    """

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)  # Пользователь устанавливается автоматически
        validators = [HabitValidator(fields=None)]  # Применяем валидаторы

    def __init__(self, *args, **kwargs):
        # Передаем instance в валидатор для корректной работы при PATCH-запросах
        super().__init__(*args, **kwargs)
        self.validators = [HabitValidator(fields=self.instance)]