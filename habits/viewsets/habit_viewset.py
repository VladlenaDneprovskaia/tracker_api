from datetime import timedelta

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.serializers import HabitSerializer


@extend_schema(tags=['Habit API'])
class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer

    @action(detail=True, methods=['get'], url_path='stats')
    def get_stats(self, request, pk=None):
        habit = self.get_object()
        checkins = habit.checkin_set.order_by('created_at').all()

        total_checkins = checkins.count()

        streak = 1
        total_streak = 1
        last_checkin = None

        for checkin in checkins:
            is_streak = last_checkin is not None and checkin.created_at - last_checkin.created_at <= timedelta(days=1)
            streak = streak + 1 if is_streak else 1
            total_streak = max(streak, total_streak)
            last_checkin = checkin

        data = {
            'habit_id': habit.id,
            'name': habit.name,
            'total_checkins': total_checkins,
            'total_streak': total_streak,
            'current_streak': streak,
        }

        return Response(data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
