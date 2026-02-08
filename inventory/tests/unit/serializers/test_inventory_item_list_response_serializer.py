from inventory.api.serializers.inventory_item_list_response_serializer import (
    InventoryItemListResponseSerializer,
)


def test_inventory_item_list_request_response_serializer_success():
    payload = {
        "success": True,
        "result": [
            {"item_code": "ROD_BASIC", "item_name": "Basic Rod", "quantity": 1},
        ],
    }
    serializer = InventoryItemListResponseSerializer(data=payload)
    assert serializer.is_valid()
