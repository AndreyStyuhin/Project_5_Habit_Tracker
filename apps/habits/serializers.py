from rest_framework import serializers
from apps.habits.models import Habit
from apps.habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Привычки.
    """

    # Добавляем поле для отображения информации о пользователе (только для чтения)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'last_sent_time')  # Пользователь и время отправки устанавливаются автоматически

    def validate(self, data):
        """
        Валидация данных привычки.
        """
        # Передаем текущий instance (если есть) в валидатор
        validator = HabitValidator(instance=self.instance)
        validator(data)
        return data

    def to_representation(self, instance):
        """
        Кастомизация отображения данных.
        """
        representation = super().to_representation(instance)

        # Для related_habit показываем ID и действие
        if instance.related_habit:
            representation['related_habit'] = {
                'id': instance.related_habit.id,
                'action': instance.related_habit.action
            }

        # Добавляем информацию о пользователе
        representation['user'] = {
            'id': instance.user.id,
            'email': instance.user.email
        }

        return representation

    def create(self, validated_data):
        """
        Создание привычки с автоматической привязкой к пользователю.
        """
        # Пользователь уже должен быть установлен в perform_create ViewSet
        # Этот метод оставляем на случай дополнительной логики
        return super().create(validated_data)
