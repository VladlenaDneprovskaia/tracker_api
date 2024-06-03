from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        exclude = ('user',)

    def create(self, validated_data):
        return Habit.objects.create(user_id=self.context.get('user_id'), **validated_data)
