from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from coaches.models import Coach, Mentee
from coaches.serializers import CoachSerializer


@extend_schema(tags=['Coach API'])
class CoachViewSet(ReadOnlyModelViewSet):
    serializer_class = CoachSerializer

    def get_queryset(self):
        myself = self.request.query_params.get('myself', False)

        if self.request.user.is_authenticated and myself:
            return Coach.objects.filter(user=self.request.user)

        return Coach.objects.all()

    @action(detail=True, methods=['POST'])
    def add_coach(self, request, pk):
        coach = Coach.objects.filter(pk=pk).first()
        if coach is None:
            return Response('Coach not found', status=status.HTTP_404_NOT_FOUND)

        Mentee.objects.create(user=request.user, coach=coach)
        return Response('Coach added', status=status.HTTP_201_CREATED)
