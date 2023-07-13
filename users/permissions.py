from rest_framework.permissions import BasePermission


class AdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == "admin"