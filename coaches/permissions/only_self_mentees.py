from rest_framework import permissions


class OnlySelfMentees(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and str(user.coach.id) == view.kwargs['coach_pk']
