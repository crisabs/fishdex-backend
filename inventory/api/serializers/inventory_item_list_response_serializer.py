from rest_framework import serializers


class InventoryItemListResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = serializers.DictField()
