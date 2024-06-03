from rest_framework.serializers import ModelSerializer

from coaches.models import Mentee
from coaches.serializers import CoachSerializer
from tracker.serializers import UserSerializer


class MenteeSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    coach = CoachSerializer(read_only=True)

    class Meta:
        model = Mentee
        fields = '__all__'
