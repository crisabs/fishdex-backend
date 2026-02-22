from rest_framework import serializers


class InventoryFisherFishDescriptionResponseSerializer(serializers.Serializer):
    """
    Serializer for the inventory fisher fish description response.

    This serializer is used to validate the output data
    for the inventory fisher fish description endpoint.
    """

    success = serializers.BooleanField()
