from rest_framework import serializers


class BuyItemRequestSerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=15)
    quantity = serializers.IntegerField(min_value=1)
