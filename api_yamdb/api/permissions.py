from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Класс проверки доступа для админа и суперюзера."""

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_admin


class IsAdminOrReadOnly(IsAdmin):
    """
    Класс проверки доступа админа и суперюзера, либо остальным,
    но только для чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAuthorOrIsAdminOrIsModeratorOrRead(IsAdmin):
    """Класс проверки доступа для автора и модератора."""

    def has_permission(self, request, view):
        """
        Метод разрешений.
        Переопределение базового метода разрешения на уровне запроса.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Метод разрешений.
        Метод определяет разрешения на уровне объекта.
        """
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_moderator
            or super().has_permission(request, view)
        )
