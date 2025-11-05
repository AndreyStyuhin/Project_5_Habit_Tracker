from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации (создания) нового пользователя.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
