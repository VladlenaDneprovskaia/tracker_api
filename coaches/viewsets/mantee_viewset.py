from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from coaches.models import Mentee
from coaches.permissions import IsCoach, OnlySelfMentees
from coaches.serializers import MenteeSerializer
from habits.serializers import HabitSerializer


@extend_schema(tags=['Mentees API'])
class MenteeViewSet(ReadOnlyModelViewSet, DestroyModelMixin):
    serializer_class = MenteeSerializer
    permission_classes = (IsCoach, OnlySelfMentees)

    @action(detail=True, methods=['GET'])
    def habits(self, request, pk=None, coach_pk=None):
        mentee = Mentee.objects.filter(pk=pk, coach_id=coach_pk).first()

        if mentee is None:
            return Response("Mentee is not found", status=status.HTTP_404_NOT_FOUND)

        data = HabitSerializer(mentee.user.habit_set, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Mentee.objects.filter(coach=self.request.user.coach)
