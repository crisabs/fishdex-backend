from rest_framework import serializers


class InventoryFisherFishDescriptionRequestSerializer(serializers.Serializer):
    """
    Serializer for the inventory fisher fish description request.

    This serializer is used to validate the input data for
    the inventory fisher fish description endpoint.
    """

    pk = serializers.IntegerField(min_value=1)
    description = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
