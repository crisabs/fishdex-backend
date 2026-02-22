from inventory.api.serializers.inventory_fisher_fish_description_request_serializer import (
    InventoryFisherFishDescriptionRequestSerializer,
)


class TestInventoryFisherFishDescriptionRequestSerializerSuccess:
    def test_inventory_fisher_fish_description_request_serializer_success(self):
        """
        Test the InventoryFisherFishDescriptionRequestSerializer with valid data.
        """
        data = {"pk": 1, "description": "A nice fish"}

        serializer = InventoryFisherFishDescriptionRequestSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == data


class TestInventoryFisherFishDescriptionRequestSerializerErrors:
    def test_inventory_fisher_fish_description_request_serializer_invalid_pk(self):
        """
        Test the InventoryFisherFishDescriptionRequestSerializer with invalid pk.
        """
        data = {"pk": 0, "description": "A nice fish"}

        serializer = InventoryFisherFishDescriptionRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "pk" in serializer.errors

    def test_inventory_fisher_fish_description_request_serializer_invalid_description(
        self,
    ):
        """
        Test the InventoryFisherFishDescriptionRequestSerializer with invalid description.
        """
        data = {"pk": 1, "description": "A" * 256}

        serializer = InventoryFisherFishDescriptionRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_inventory_fisher_fish_description_request_serializer_error_missing_pk(
        self,
    ):
        """
        Test the InventoryFisherFishDescriptionRequestSerializer with missing pk.
        """
        data = {"description": "A nice fish"}

        serializer = InventoryFisherFishDescriptionRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "pk" in serializer.errors

    def test_inventory_fisher_fish_description_request_serializer_error_missing_description(
        self,
    ):
        """
        Test the InventoryFisherFishDescriptionRequestSerializer with missing description.
        """
        data = {"pk": 1}

        serializer = InventoryFisherFishDescriptionRequestSerializer(data=data)
        assert not serializer.is_valid(), serializer.errors
        assert "description" in serializer.errors
