from rest_framework import serializers


class RegistrationRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    is_coach = serializers.BooleanField(required=True)
