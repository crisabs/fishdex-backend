from rest_framework import serializers


class FishDetailsRequestSerializer(serializers.Serializer):
    fish_id = serializers.IntegerField(min_value=0, max_value=100)
