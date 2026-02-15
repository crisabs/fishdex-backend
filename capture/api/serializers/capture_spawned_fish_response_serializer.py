from rest_framework import serializers


class CaptureSpawnedFishResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = serializers.CharField()
