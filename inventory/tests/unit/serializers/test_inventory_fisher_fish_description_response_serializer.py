from inventory.api.serializers.inventory_fisher_fish_description_response_serializer import (
    InventoryFisherFishDescriptionResponseSerializer,
)


def test_inventory_fisher_fish_description_response_serializer_success():
    """
    Test the InventoryFisherFishDescriptionResponseSerializer with valid data.
    """

    data = {"success": True}

    serializer = InventoryFisherFishDescriptionResponseSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == data


def test_inventory_fisher_fish_description_response_serializer_invalid():
    """
    Test the InventoryFisherFishDescriptionResponseSerializer with invalid data.
    """

    data = {"success": "not a boolean"}

    serializer = InventoryFisherFishDescriptionResponseSerializer(data=data)
    assert not serializer.is_valid()
    assert "success" in serializer.errors


def test_inventory_fisher_fish_description_response_serializer_missing_field():
    """
    Test the InventoryFisherFishDescriptionResponseSerializer with missing required field.
    """

    data = {}

    serializer = InventoryFisherFishDescriptionResponseSerializer(data=data)
    assert not serializer.is_valid()
    assert "success" in serializer.errors
