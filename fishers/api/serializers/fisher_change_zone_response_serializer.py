from rest_framework import serializers


class FisherChangeZoneResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
    new_zone = serializers.CharField()
