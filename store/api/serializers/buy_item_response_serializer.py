from rest_framework import serializers


class BuyItemResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = serializers.CharField()
