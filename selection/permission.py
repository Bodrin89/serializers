from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    """Проверка совпадения автора подборки и того кто ее изменяет"""

    message = "You are not the author"

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
