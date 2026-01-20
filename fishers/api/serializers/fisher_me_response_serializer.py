from rest_framework import serializers


class FisherMeResponseSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    level = serializers.IntegerField(min_value=0)
