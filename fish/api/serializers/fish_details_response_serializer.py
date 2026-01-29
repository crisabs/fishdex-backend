from rest_framework import serializers


class FishDetailsSerializer(serializers.Serializer):
    fish_id = serializers.IntegerField(min_value=0, max_value=100)
    name = serializers.CharField()
    description = serializers.CharField(max_length=100)
    habitat = serializers.CharField(max_length=15)
    rarity = serializers.CharField(max_length=15)
    base_weight = serializers.FloatField()
    base_price = serializers.FloatField()


class FishDetailsResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = FishDetailsSerializer()
