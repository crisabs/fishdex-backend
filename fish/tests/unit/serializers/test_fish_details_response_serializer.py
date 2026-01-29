from fish.api.serializers.fish_details_response_serializer import (
    FishDetailsResponseSerializer,
)


def test_fish_details_response_serializer_success():
    payload = {
        "success": True,
        "result": {
            "fish_id": 9,
            "name": "Largemouth Bass",
            "description": "A popular sport fish with powerful strikes.",
            "habitat": "LAKE",
            "rarity": "RARE",
            "base_weight": 3.5,
            "base_price": 30.0,
        },
    }
    serializer = FishDetailsResponseSerializer(data=payload)
    assert serializer.is_valid()


def test_fish_details_response_serializer_without_result():
    payload = {
        "success": True,
    }
    serializer = FishDetailsResponseSerializer(data=payload)
    assert not serializer.is_valid()


def test_fish_details_response_serializer_without_success():
    payload = {
        "result": {
            "fish_id": 9,
            "name": "Largemouth Bass",
            "description": "A popular sport fish with powerful strikes.",
            "habitat": "LAKE",
            "rarity": "RARE",
            "base_weight": 3.5,
            "base_price": 30.0,
        },
    }
    serializer = FishDetailsResponseSerializer(data=payload)
    assert not serializer.is_valid()
