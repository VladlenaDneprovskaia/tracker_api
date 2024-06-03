from rest_framework.serializers import ModelSerializer

from coaches.models import Recommendation


class RecommendationSerializer(ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('id', 'message', 'mentee_id', 'coach_id')

    def create(self, validated_data):
        return Recommendation.objects.create(coach_id=self.context['coach_id'],
                                             mentee_id=self.context['mentee_id'],
                                             **validated_data)
