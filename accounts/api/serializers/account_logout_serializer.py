from rest_framework import serializers


class AccountLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
