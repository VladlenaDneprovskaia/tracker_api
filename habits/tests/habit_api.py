from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from habits.models import Habit, CheckIn
from habits.serializers import HabitSerializer


def get_url_stats(habit):
    return f'/api/habits/{habit.id}/stats/'


class HabitApiTest(APITestCase):
    url = '/api/habits/'

    def setUp(self):
        self.test_user = User.objects.create_user(
            username="<USERNAME>", email="<EMAIL>", password="<PASSWORD>")

        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.client.login(username="<USERNAME>", password="<PASSWORD>")

    def test_get_habit_should_return_403_status_code_when_logout(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_habits_should_return_yourself_user_habits(self):
        second_user = User.objects.create_user(
            username="<SECOND USERNAME>", email="<SECOND EMAIL>", password="<PASSWORD>")

        self_user_habits = [
            Habit.objects.create(name="Habit 1", description="<DESCRIPTION>", frequency="DD", user=self.test_user),
            Habit.objects.create(name="Habit 2", description="<DESCRIPTION>", frequency="DD", user=self.test_user),
            Habit.objects.create(name="Habit 3", description="<DESCRIPTION>", frequency="DD", user=self.test_user),
        ]

        other_user_habits = [
            Habit.objects.create(name="Habit 4", description="<DESCRIPTION>", frequency="DD", user=second_user),
            Habit.objects.create(name="Habit 5", description="<DESCRIPTION>", frequency="DD", user=second_user),
        ]

        response = self.client.get(self.url)
        expected_data = HabitSerializer(self_user_habits, many=True).data

        self.assertEqual(response.data['results'], expected_data)
        for habit in other_user_habits:
            serialized_habit = HabitSerializer(habit).data
            self.assertNotIn(serialized_habit, response.data['results'])

    def test_get_habits_stats_should_return_valid_value(self):
        habit = Habit.objects.create(name="<HABIT>", description="<DESCRIPTION>", frequency="DD", user=self.test_user)

        checkins = [
            CheckIn.objects.create(habit=habit),
            CheckIn.objects.create(habit=habit),
            CheckIn.objects.create(habit=habit),
            CheckIn.objects.create(habit=habit),
        ]

        for i in range(len(checkins)):
            if i == len(checkins) - 2:
                checkins[i].created_at = datetime.now(timezone.utc) + timedelta(days=i)
            else:
                checkins[i].created_at = datetime.now(timezone.utc) - timedelta(days=i)
            checkins[i].save()

        url = get_url_stats(habit)

        expected_data = {
            'habit_id': habit.id,
            'name': '<HABIT>',
            'total_checkins': 4,
            'total_streak': 2,
            'current_streak': 1,
        }

        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
