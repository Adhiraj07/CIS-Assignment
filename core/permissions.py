from rest_framework import permissions

class IsAdminOrManager(permissions.BasePermission):
    """
    Allows access only to admin or manager users.
    """
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'MANAGER']

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'
