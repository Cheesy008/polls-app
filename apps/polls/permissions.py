from rest_framework import permissions


class IsPollOwnerOrReadOnly(permissions.BasePermission):
    """
    Пермишен, чтобы позволить изменять опрос только его создателю.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    """
    Пермишен, чтобы позволить смотреть опросы всем пользователям,
    но изменять только админам.
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
