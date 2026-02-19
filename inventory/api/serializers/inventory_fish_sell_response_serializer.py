from rest_framework import serializers


class InventoryFishSellResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
