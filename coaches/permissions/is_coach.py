from rest_framework import permissions


class IsCoach(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and hasattr(user, 'coach')
