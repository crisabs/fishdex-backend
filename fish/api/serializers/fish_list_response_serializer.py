from rest_framework import serializers
from typing import ClassVar


class FishSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    fish_id = serializers.IntegerField(min_value=1)
    description = serializers.CharField(max_length=100)
    habitat = serializers.CharField(max_length=15)
    rarity = serializers.CharField(max_length=15)
    base_weight = serializers.FloatField()
    base_price = serializers.FloatField()


class FishListResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    data: ClassVar[serializers.ListSerializer] = serializers.ListSerializer(
        child=FishSerializer()
    )
