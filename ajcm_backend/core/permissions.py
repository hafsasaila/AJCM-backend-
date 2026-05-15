from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Accès réservé aux administrateurs"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'

class IsMember(permissions.BasePermission):
    """Accès réservé aux membres"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'MEMBER'

class IsMemberOrAdmin(permissions.BasePermission):
    """Accès aux membres et administrateurs"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['MEMBER', 'ADMIN']