from inventory.api.serializers.inventory_fish_list_response_serializer import (
    InventoryFishListResponseSerializer,
)


def test_inventory_fish_list_response_serializer_success():
    """
    GIVEN a valid inventory fish list payload
    WHEN the response serializer serializers the payload
    THEN it returns the expected JSON structure following the API contract
    """
    payload = {
        "success": True,
        "result": [
            {
                "fish_name": "Salmon",
                "price": 4,
                "weight": "0.30",
                "caught_at": "2026-02-10T05:52:57.267600Z",
                "rarity": "COMMON",
            },
        ],
    }
    serializer = InventoryFishListResponseSerializer(payload)
    serializer_data = dict(serializer.data)
    assert serializer_data["success"] is True
    assert serializer_data["result"][0]["fish_name"] == "Salmon"
    assert serializer_data["result"][0] == {
        "fish_name": "Salmon",
        "price": 4,
        "weight": "0.30",
        "caught_at": "2026-02-10T05:52:57.267600Z",
        "rarity": "COMMON",
    }


def test_inventory_fish_list_response_serializer_error_requires_result():
    """
    GIVEN an invalid payload missing the result field
    WHEN the response serializer validates the input data
    THEN it reports a validation error for the required result field
    """
    payload = {
        "success": True,
    }
    serializer = InventoryFishListResponseSerializer(data=payload)
    assert not serializer.is_valid()
    assert "result" in serializer.errors
