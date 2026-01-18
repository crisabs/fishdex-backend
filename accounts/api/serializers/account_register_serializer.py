from rest_framework import serializers


class AccountRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
