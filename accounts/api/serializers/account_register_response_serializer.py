from rest_framework import serializers


class AccountRegisterResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    data = serializers.CharField()  # type: ignore
