from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from inventory.domain.services.inventory_service import (
    get_inventory_item_list,
    get_inventory_fish_list,
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

        response_serializer = InventoryFishListResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
