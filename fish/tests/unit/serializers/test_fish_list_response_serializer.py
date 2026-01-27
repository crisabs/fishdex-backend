from fish.api.serializers.fish_list_response_serializer import (
    FishListResponseSerializer,
)


def test_fish_list_response_serializer_success():
    payload = {
        "success": True,
        "results": [
            {
                "id": 1,
                "name": "Salmon",
                "fish_id": 1,
                "description": "A vary tasty river fish",
                "habitat": "RIVER",
                "rarity": "COMMON",
                "base_weight": 0.45,
                "base_price": 9.8,
            }
        ],
    }
    serializer = FishListResponseSerializer(data=payload)
    assert serializer.is_valid()


def test_fish_list_response_serializer_missing_result():
    payload = {
        "success": True,
        "results": [{}],
    }
    serializer = FishListResponseSerializer(data=payload)
    assert not serializer.is_valid()
