from rest_framework import permissions

class IsAdminOrmanager(permissions.BasePermission):
    """
    Only manager and admin can access.
    """
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'MANAGER']

class IsAdmin(permissions.BasePermission):
    """
    Only admin can access.
    """
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'
