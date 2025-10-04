from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Разрешение для модераторов.
    Модераторы могут просматривать и редактировать любые курсы и уроки,
    но не могут создавать и удалять.
    """
    def has_permission(self, request, view):
        # Модераторы НЕ могут создавать и удалять
        # Проверяем action только если он существует (ViewSet)
        if hasattr(view, 'action') and view.action in ['create', 'destroy']:
            return False
        # Для Generic views проверяем HTTP метод
        if request.method in ['POST', 'DELETE']:
            return False
        return request.user.is_authenticated and request.user.groups.filter(name='Модераторы').exists()

class IsOwner(permissions.BasePermission):
    """
    Разрешение для владельцев объектов.
    Владельцы могут выполнять любые операции со своими объектами.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModeratorOrOwner(permissions.BasePermission):
    """
    Разрешение для модераторов или владельцев.
    Модераторы могут выполнять любые операции.
    Владельцы могут выполнять любые операции со своими объектами.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        return obj.owner == request.user

class IsModeratorOrOwnerForModify(permissions.BasePermission):
    """
    Разрешение для модераторов или владельцев при модификации.
    Для безопасных методов (GET, HEAD, OPTIONS) доступ всем авторизованным.
    Для модификации (POST, PUT, PATCH, DELETE) - только модераторам или владельцам.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        return obj.owner == request.user

class IsNotModerator(permissions.BasePermission):
    """
    Разрешение для обычных пользователей (НЕ модераторов).
    Модераторы НЕ могут создавать новые объекты.
    """
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модераторы').exists():
            return False
        return True
