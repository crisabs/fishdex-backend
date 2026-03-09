from rest_framework import serializers


class FisherMeResponse(serializers.Serializer):
    nickname = serializers.CharField()
    level = serializers.IntegerField()
    coins = serializers.IntegerField()
    current_zone = serializers.CharField()


class FishersFisherMeResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = FisherMeResponse()
