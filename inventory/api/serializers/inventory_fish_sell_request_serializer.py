from rest_framework import serializers


class InventoryFishSellRequestSerializer(serializers.Serializer):
    fish_id = serializers.IntegerField(min_value=1, max_value=100)
    pk = serializers.IntegerField(min_value=0)
    total_weight = serializers.DecimalField(max_digits=5, decimal_places=2)
