from rest_framework import serializers

ITEM_CODES_ROD = {
    "Basic Rod": "ROD_BASIC",
    "Super Rod": "ROD_SUPER",
    "Ultra Rod": "ROD_ULTRA",
}

ITEM_CODES_BAIT = {
    "Basic Bait": "BAIT_BASIC",
    "Super Bait": "BAIT_SUPER",
    "Ultra Bait": "BAIT_ULTRA",
}


class CaptureFishRequestSerializer(serializers.Serializer):
    used_rod = serializers.ChoiceField(
        choices=[(v, k) for k, v in ITEM_CODES_ROD.items()]
    )
    used_bait = serializers.ChoiceField(
        choices=[(v, k) for k, v in ITEM_CODES_BAIT.items()]
    )
    fish_id = serializers.IntegerField(min_value=1, max_value=200)
    fish_weight = serializers.FloatField(min_value=0.0)
    fish_length = serializers.FloatField(min_value=0.0)
