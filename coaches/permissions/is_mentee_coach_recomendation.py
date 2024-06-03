from rest_framework import permissions

from coaches.models import Mentee


class IsMenteeCoachRecommendation(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if hasattr(user, 'mentee') and str(user.mentee.id) == view.kwargs['mentee_pk']:
            return str(user.mentee.coach.id) == view.kwargs['coach_pk'] and (
                        request.method == 'GET' or request.method == 'DELETE')

        if hasattr(user, 'coach') and str(user.coach.id) == view.kwargs['coach_pk']:
            mentee = Mentee.objects.filter(coach__id=view.kwargs['coach_pk'], id=view.kwargs['mentee_pk']).first()
            return mentee is not None

        return False
