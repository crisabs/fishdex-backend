from rest_framework import serializers


class CaptureSpawnedFish(serializers.Serializer):
    fish_id = serializers.IntegerField()
    name = serializers.CharField()
    total_weight = serializers.DecimalField(max_digits=4, decimal_places=2)
    habitat = serializers.CharField()
    base_price = serializers.FloatField()


class CaptureSpawnedFishResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = CaptureSpawnedFish()
