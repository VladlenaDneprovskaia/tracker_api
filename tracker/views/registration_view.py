from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from coaches.models import Coach
from tracker.serializers import UserSerializer, RegistrationRequestSerializer

UserModel = get_user_model()


@extend_schema(
    tags=['Auth API'],
    request=RegistrationRequestSerializer,
    responses={
        '201': {'type': 'object', 'properties': {
            'id': {'type': 'integer'},
            'username': {'type': 'string'},
            'access': {'type': 'string'},
            'refresh': {'type': 'string'},
        }}})
class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        body = RegistrationRequestSerializer(data=request.data)

        if body.is_valid():
            is_coach = body.data.pop('is_coach', False)
            user_serializer = UserSerializer(data=body.data)

            if user_serializer.is_valid():
                user = user_serializer.save()

                refresh = RefreshToken.for_user(user)
                data = {**user_serializer.data, **{'refresh': str(refresh), 'access': str(refresh.access_token)}}

                if is_coach:
                    coach = Coach.objects.create(user=user)
                    coach.save()

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(body.errors, status=status.HTTP_400_BAD_REQUEST)
