from drf_spectacular.utils import extend_schema

from coaches.models import Recommendation
from coaches.permissions import IsMenteeCoachRecommendation
from coaches.serializers import RecommendationSerializer
from tracker.viewsets import ImmutableModelViewSet


@extend_schema(tags=['Recommendation API'])
class RecommendationViewSet(ImmutableModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = (IsMenteeCoachRecommendation,)

    # def create(self, request, *args, **kwargs):
    #     serializer = RecommendationSerializer(
    #         data={**request.data, **{'coach_pk': kwargs['coach_pk'], 'mentee_pk': kwargs['mentee_pk']}})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'mentee_id': self.kwargs.get('mentee_pk'), 'coach_id': self.kwargs.get('coach_pk')}

    def get_queryset(self):
        return Recommendation.objects.filter(mentee__id=self.kwargs['mentee_pk'], coach__id=self.kwargs['coach_pk'])
