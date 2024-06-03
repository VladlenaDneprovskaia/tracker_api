from rest_framework.serializers import ModelSerializer

from habits.models import CheckIn


class CheckInSerializer(ModelSerializer):
    class Meta:
        model = CheckIn
        exclude = ('habit',)

    def create(self, validated_data):
        return CheckIn.objects.create(habit_id=self.context.get('habit_id'), **validated_data)
