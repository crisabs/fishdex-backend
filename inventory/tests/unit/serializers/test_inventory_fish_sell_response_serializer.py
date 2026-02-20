from inventory.api.serializers.inventory_fish_sell_response_serializer import (
    InventoryFishSellResponseSerializer,
)


def test_inventory_fish_sell_response_serializer_success():
    serializer = InventoryFishSellResponseSerializer(data={"code": "OK"})
    assert serializer.is_valid()
