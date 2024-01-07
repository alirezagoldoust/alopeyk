from rest_framework.permissions import BasePermission

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.all()[0].name == 'Driver')