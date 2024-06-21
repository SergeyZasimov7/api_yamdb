from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Класс проверки доступа для админа и суперюзера."""

    def is_admin(self, user):
        return user.is_authenticated and (user.is_superuser or user.is_admin)

    def has_permission(self, request, view):
        return self.is_admin(request.user)


class IsAdminOrReadOnly(IsAdmin):
    """
    Класс проверки доступа админа и суперюзера, либо остальным,
    но только для чтения.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class ThisAuthorOrReadOnly(permissions.BasePermission):
    """Класс разрешений."""

    def has_object_permission(self, request, view, obj):
        """
        Метод разрешений.
        Метод определяет разрешения на уровне объекта.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin or request.user.is_moderator
        )
