from datetime import datetime, timezone, timedelta

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound

from habits.models import CheckIn, Habit
from habits.serializers import CheckInSerializer
from tracker.viewsets import ImmutableModelViewSet

timedelta_by_habit_frequency = {
    'DD': timedelta(days=1),
    'WW': timedelta(weeks=1),
    'MM': timedelta(days=30),
    'YY': timedelta(days=365),
}


@extend_schema(tags=['CheckIn API'])
class CheckInViewSet(ImmutableModelViewSet):
    serializer_class = CheckInSerializer

    def create(self, request, *args, **kwargs):
        habit = Habit.objects.filter(pk=kwargs['habit_pk']).first()

        if habit is None:
            raise NotFound(detail='Habit not found', code=status.HTTP_404_NOT_FOUND)

        last_checkin = CheckIn.objects.filter(habit=habit).order_by('-created_at').first()

        if last_checkin is not None:
            current_delta_time = datetime.now(timezone.utc) - last_checkin.created_at

            if current_delta_time <= timedelta_by_habit_frequency[habit.frequency]:
                raise ParseError(detail='Not enough time has passed', code=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return CheckIn.objects.filter(habit=self.kwargs['habit_pk'])

    def get_serializer_context(self):
        return {'habit_id': self.kwargs['habit_pk']}
