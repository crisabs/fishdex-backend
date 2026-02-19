from inventory.api.serializers.inventory_fish_sell_request_serializer import (
    InventoryFishSellRequestSerializer,
)


def test_inventory_fish_sell_request_serializer_valid_data():
    """
    Test that the serializer correctly validates
    valid data and does not raise any errors.
    """

    data = {"fish_id": 10, "pk": 1, "total_weight": "25.50"}
    serializer = InventoryFishSellRequestSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


def test_inventory_fish_sell_request_serializer_invalid_data():
    """
    Test that the serializer correctly identifies
    invalid data and provides appropriate error messages.
    """

    data = {"fish_id": 150, "pk": -1, "total_weight": "abc"}
    serializer = InventoryFishSellRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert "fish_id" in serializer.errors
    assert "pk" in serializer.errors
    assert "total_weight" in serializer.errors


def test_inventory_fish_sell_request_serializer_missing_fields():
    """
    Test that the serializer correctly identifies
    missing required fields and provides appropriate error messages.
    """

    data = {"fish_id": 10}
    serializer = InventoryFishSellRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert "pk" in serializer.errors
    assert "total_weight" in serializer.errors


def test_inventory_fish_sell_request_serializer_edge_cases():
    """
    Test edge cases for the serializer,
    such as minimum and maximum values for fields.
    """

    data = {"fish_id": 1, "pk": 0, "total_weight": "0.00"}
    serializer = InventoryFishSellRequestSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    data = {"fish_id": 100, "pk": 999, "total_weight": "999.99"}
    serializer = InventoryFishSellRequestSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
