from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Класс проверки доступа для админа и суперюзера."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Класс проверки доступа админа и суперюзера, либо остальным,
    но только для чтения.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin
                    or request.user.is_superuser)))


class IsAdminOrSuperuser(permissions.BasePermission):
    """Разрешение для доступа только администраторам или суперпользователям."""
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_admin


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
            or request.user.is_admin or request.user.is_moderator)