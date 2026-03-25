from rest_framework import serializers


class BaitResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()


class GetBaitListResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = BaitResponseSerializer(many=True)
