from rest_framework import serializers


class _InventoryItemList(serializers.Serializer):
    item_code = serializers.CharField()
    item_name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)


class InventoryItemListResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = _InventoryItemList(many=True)
