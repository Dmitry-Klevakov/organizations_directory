from rest_framework import permissions


class IsAdminOrIsAuthenticated(permissions.BasePermission):
    """
    Разрешает доступ только аутентифицированным пользователям,
    а изменение только администраторам.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)
