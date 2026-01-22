from rest_framework import serializers


class FisherNicknameResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
