from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from habits.models import CheckIn, Habit
from habits.serializers import CheckInSerializer


def get_url(habit, checkin=None):
    if checkin:
        return f'/api/habits/{habit.id}/checkins/{checkin.id}/'
    return f'/api/habits/{habit.id}/checkins/'


def create_habit(user, habit_name=None):
    return Habit.objects.create(name=habit_name if habit_name else "<HABIT>",
                                description="<HABIT>",
                                frequency="DD",
                                user=user)


class CheckInApiTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username="<USERNAME>", email="<EMAIL>", password="<PASSWORD>")

        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.client.login(username="<USERNAME>", password="<PASSWORD>")

    def test_get_checkins_should_return_403_status_code_when_logout(self):
        habit = create_habit(self.test_user)
        checkin = CheckIn.objects.create(habit=habit)

        response = self.client.get(get_url(habit, checkin))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.client.logout()

        response = self.client.get(get_url(habit, checkin))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_checkins_should_return_yourself_user_habits(self):
        other_user = User.objects.create_user(username="<SECOND USERNAME>",
                                              email="<SECOND EMAIL>",
                                              password="<PASSWORD>")

        self_user_habit = create_habit(self.test_user)
        other_habit = create_habit(other_user)

        self_user_checkins = [
            CheckIn.objects.create(habit=self_user_habit),
            CheckIn.objects.create(habit=self_user_habit),
            CheckIn.objects.create(habit=self_user_habit),
        ]

        other_user_checkins = [
            CheckIn.objects.create(habit=other_habit),
            CheckIn.objects.create(habit=other_habit),
        ]

        response = self.client.get(get_url(self_user_habit))
        expected_data = CheckInSerializer(self_user_checkins, many=True).data
        self.assertEqual(response.data['results'], expected_data)

        for checkin in other_user_checkins:
            serialized_habit = CheckInSerializer(checkin).data
            self.assertNotIn(serialized_habit, response.data['results'])

        for checkin in other_user_checkins:
            response_one_other_checkin = self.client.get(get_url(self_user_habit, checkin))
            self.assertEqual(status.HTTP_404_NOT_FOUND, response_one_other_checkin.status_code)

        for checkin in self_user_checkins:
            response_one_self_checkin = self.client.get(get_url(self_user_habit, checkin))
            self.assertEqual(status.HTTP_200_OK, response_one_self_checkin.status_code)
