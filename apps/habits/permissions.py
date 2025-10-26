from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Кастомное право доступа.
    Проверяет, является ли запрашивающий пользователь владельцем объекта.
    """
    message = 'Вы не являетесь владельцем этой привычки.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user