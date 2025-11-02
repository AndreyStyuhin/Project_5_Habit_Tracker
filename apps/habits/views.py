from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.habits.models import Habit
from apps.habits.serializers import HabitSerializer
from apps.habits.permissions import IsOwner
from apps.habits.paginators import StandardPagination


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD-операций над Привычками.
    Показывает только привычки текущего пользователя.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = StandardPagination

    def get_queryset(self):
        """
        Возвращает только привычки, принадлежащие текущему пользователю.
        Для суперпользователя показываем все привычки.
        """
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        При создании привычки автоматически назначает ее владельцем текущего пользователя.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Переопределяем create для лучшего контроля над процессом создания.
        """
        # Логируем создание привычки
        print(f"🆕 Создание привычки пользователем: {request.user.email}")

        # Вызываем родительский метод
        response = super().create(request, *args, **kwargs)

        # Добавляем сообщение об успехе
        if response.status_code == status.HTTP_201_CREATED:
            print(f"✅ Привычка создана для пользователя: {request.user.email}")

        return response

    @action(detail=False, methods=['get'])
    def my_habits(self, request):
        """
        Дополнительный эндпоинт для получения ТОЛЬКО своих привычек.
        """
        habits = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Переопределяем list для добавления информации о пользователе.
        """
        response = super().list(request, *args, **kwargs)

        # Добавляем информацию о текущем пользователе в ответ
        if response.data:
            response.data['current_user'] = {
                'id': request.user.id,
                'email': request.user.email,
                'telegram_id': request.user.telegram_id
            }

        return response


class PublicHabitListAPIView(generics.ListAPIView):
    """
    Эндпоинт для просмотра списка публичных привычек.
    Доступен всем аутентифицированным пользователям.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def list(self, request, *args, **kwargs):
        """
        Переопределяем list для добавления информации о пользователе.
        """
        response = super().list(request, *args, **kwargs)

        # Добавляем информацию о текущем пользователе
        response.data['current_user'] = {
            'id': request.user.id,
            'email': request.user.email
        }

        return response
