from rest_framework import serializers


class FisherChangeZoneRequestSerializer(serializers.Serializer):
    new_zone = serializers.CharField()
