from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner
from .paginators import StandardPagination


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD-операций над Привычками.
    Показывает только привычки текущего пользователя.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = StandardPagination  # Используем кастомный или стандартный (PageNumberPagination)

    def get_queryset(self):
        """Возвращает только привычки, принадлежащие текущему пользователю."""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании привычки автоматически назначает ее владельцем текущего пользователя."""
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """
    Эндпоинт для просмотра списка публичных привычек.
    Доступен всем аутентифицированным пользователям.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [IsAuthenticated] # По заданию "Пользователь может видеть список"
    pagination_class = StandardPagination