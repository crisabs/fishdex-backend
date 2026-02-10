from rest_framework import serializers


class _ResultResponseSerializer(serializers.Serializer):
    captured = serializers.BooleanField()
    message = serializers.CharField()


class CaptureFishResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = _ResultResponseSerializer()
