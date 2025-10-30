from rest_framework.serializers import ValidationError
from .models import Habit


class HabitValidator:
    """
    Набор валидаторов для модели Привычки.
    Применяется в сериализаторе.
    """

    def __init__(self, instance=None):
        self.instance = instance

    def __call__(self, data):
        # Объединяем данные для валидации
        full_data = {}
        if self.instance:
            # При обновлении - берем существующие значения и обновляем новыми данными
            full_data = {
                'related_habit': self.instance.related_habit,
                'reward': self.instance.reward,
                'duration': self.instance.duration,
                'is_pleasant': self.instance.is_pleasant,
                'periodicity': self.instance.periodicity,
            }

        # Обновляем full_data данными из запроса
        full_data.update(data)

        related_habit = full_data.get('related_habit')
        reward = full_data.get('reward')
        duration = full_data.get('duration')
        is_pleasant = full_data.get('is_pleasant', False)
        periodicity = full_data.get('periodicity', 1)

        # 1. Исключить одновременный выбор связанной привычки и вознаграждения
        if related_habit and reward:
            raise ValidationError(
                'Нельзя одновременно выбирать связанную привычку и указывать вознаграждение.'
            )

        # 2. Время выполнения должно быть не больше 120 секунд
        if duration and duration > 120:
            raise ValidationError(
                'Время выполнения привычки не может быть больше 120 секунд.'
            )

        # 3. В связанные привычки могут попадать только привычки с признаком приятной
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                'В связанные привычки могут попадать только привычки с признаком "приятной".'
            )

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки
        if is_pleasant and (reward or related_habit):
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки.'
            )

        # 5. Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        if periodicity and periodicity > 7:
            raise ValidationError(
                'Периодичность выполнения привычки не может быть реже, чем 1 раз в 7 дней (т.е. не более 7).'
            )

        # 6. Убедимся, что у полезной привычки есть ИЛИ вознаграждение ИЛИ связанная привычка
        if not is_pleasant and not reward and not related_habit:
            raise ValidationError(
                'У полезной привычки должно быть вознаграждение или связанная (приятная) привычка.'
            )