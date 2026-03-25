from rest_framework import serializers


class RodResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()


class GetRodListResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = RodResponseSerializer(many=True)
