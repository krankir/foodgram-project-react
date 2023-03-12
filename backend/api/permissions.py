from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Разрешение для админа или чтение для всех остальных."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_staff)


class IsAdminAuthorOrReadOnly(BasePermission):
    """Разрешение для администратора или автора, остальные только чтение."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
