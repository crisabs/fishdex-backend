from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from inventory.domain.services.inventory_service import (
    get_inventory_item_list,
    get_inventory_fish_list,
    sell_fish,
    set_description_fisher_fish,
)
from inventory.api.serializers.inventory_item_list_request_serializer import (
    InventoryItemListRequestSerializer,
)
from inventory.api.serializers.inventory_item_list_response_serializer import (
    InventoryItemListResponseSerializer,
)
from inventory.api.serializers.inventory_fish_list_request_serializer import (
    InventoryFishListRequestSerializer,
)
from inventory.api.serializers.inventory_fish_list_response_serializer import (
    InventoryFishListResponseSerializer,
)
from inventory.api.serializers.inventory_fish_sell_request_serializer import (
    InventoryFishSellRequestSerializer,
)
from inventory.api.serializers.inventory_fish_sell_response_serializer import (
    InventoryFishSellResponseSerializer,
)
from inventory.api.serializers.inventory_fisher_fish_description_request_serializer import (
    InventoryFisherFishDescriptionRequestSerializer,
)
from inventory.api.serializers.inventory_fisher_fish_description_response_serializer import (
    InventoryFisherFishDescriptionResponseSerializer,
)


class InventoryItemListView(GenericAPIView):
    """
    Retrieve the inventory item list for the authenticated user.

    Requires an authenticated user with an associated fisher profile.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = InventoryItemListRequestSerializer

    @extend_schema(
        request=InventoryItemListRequestSerializer,
        responses=InventoryItemListResponseSerializer,
    )
    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = get_inventory_item_list(user=request.user)
        payload = {"success": True, "result": result}

        response_serializer = InventoryItemListResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)


class InventoryFishListView(GenericAPIView):
    """
    Retrieve the inventory fish list for the authenticated user.

    Requires an authenticated user with an associated fisher profile.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = InventoryFishListRequestSerializer

    @extend_schema(
        request=InventoryFishListRequestSerializer,
        responses=InventoryFishListResponseSerializer,
    )
    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = get_inventory_fish_list(user=request.user)
        payload = {"success": True, "result": result}

        response_serializer = InventoryFishListResponseSerializer(payload)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class InventoryFishSellAPIView(GenericAPIView):
    """
    Sell a fish (or part of its weight) from the authenticated user's inventory.

    This endpoint allows an authenticated user to sell a specific fish from their
    inventory by providing the inventory record identifier, the fish identifier,
    and the weight to be sold.

    Permissions:
        - Authenticated users only.

    Request body:
        - pk (int): Inventory record identifier.
        - fish_id (int): Identifier of the fish to be sold.
        - total_weight (float): Weight of the fish to sell.

    Responses:
        - 200 OK: Fish sale successfully processed.
        - 400 Bad Request: Invalid input data.
        - 401 Unauthorized: Authentication credentials were not provided or are invalid.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = InventoryFishSellRequestSerializer
    extend_schema(
        request=InventoryFishSellRequestSerializer,
        responses=InventoryFishSellResponseSerializer,
    )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = sell_fish(
            user=request.user,
            pk=serializer.validated_data["pk"],
            fish_id=serializer.validated_data["fish_id"],
            total_weight=serializer.validated_data["total_weight"],
        )
        response_serializer = InventoryFishSellResponseSerializer(response)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class InventoryFisherFishDescriptionView(GenericAPIView):
    extend_schema(
        request=InventoryFisherFishDescriptionRequestSerializer,
        responses=InventoryFisherFishDescriptionResponseSerializer,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryFisherFishDescriptionRequestSerializer

    def patch(self, request):
        """
        Set the description for a fisher fish inventory record.
        This endpoint allows an authenticated user to update the description of a specific
        fisher fish inventory record by providing the record's primary key
        and the new description.
        Permissions:
            - Authenticated users only.
            Request body:
            - pk (int): Primary key of the fisher fish inventory record to update.
            - description (str): New description for the fisher fish inventory record.
        Responses:
            - 200 OK: Description successfully updated.
            - 400 Bad Request: Invalid input data.
            - 401 Unauthorized: Authentication credentials
              were not provided or are invalid.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = set_description_fisher_fish(
            user=request.user,
            pk=serializer.validated_data["pk"],
            description=serializer.validated_data["description"],
        )
        response_serializer = InventoryFisherFishDescriptionResponseSerializer(response)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
