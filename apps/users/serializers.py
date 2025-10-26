from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания (регистрации) пользователя."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'telegram_id', 'username')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            telegram_id=validated_data.get('telegram_id'),
            username=validated_data.get('username', validated_data['email'].split('@')[0])
        )
        return user