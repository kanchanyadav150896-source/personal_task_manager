from rest_framework import permissions


class IsAssignedUser(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        return obj.assigned_to == request.user