from rest_framework import permissions

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактировать/удалять только владельцу объекта или админу.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = только просмотр (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для примера: у объекта должен быть user (владелец)
        return getattr(obj, 'user', None) == request.user or request.user.is_staff