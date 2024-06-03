from rest_framework.serializers import ModelSerializer

from coaches.models import Coach
from tracker.serializers import UserSerializer


class CoachSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = ('id', 'user')
