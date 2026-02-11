from rest_framework import serializers


class _InventoryFishResponseSerializer(serializers.Serializer):
    fish_name = serializers.CharField()
    price = serializers.IntegerField()
    weight = serializers.DecimalField(decimal_places=2, max_digits=8)
    caught_at = serializers.DateTimeField()
    rarity = serializers.CharField()


class InventoryFishListResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = _InventoryFishResponseSerializer(many=True)
