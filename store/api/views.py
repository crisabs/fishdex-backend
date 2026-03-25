from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from store.domain.store_service import buy_item
from drf_spectacular.utils import extend_schema
from store.api.serializers.buy_item_request_serializer import BuyItemRequestSerializer
from store.api.serializers.buy_item_response_serializer import BuyItemResponseSerializer
from store.domain.store_service import get_rod_store_list, get_bait_store_list
from store.api.serializers.get_rod_list_request_serializer import (
    GetRodListRequestSerializer,
)
from store.api.serializers.get_rod_list_response_serializer import (
    GetRodListResponseSerializer,
)
from store.api.serializers.get_bait_list_request_serializer import (
    GetBaitListRequestSerializer,
)
from store.api.serializers.get_bait_list_response_serializer import (
    GetBaitListResponseSerializer,
)


class BuyItemAPIView(GenericAPIView):
    """
    API endpoint to purchase a store item for the authenticated user.

    Handles PUT requests, validates input via BuyItemRequestSerializer,
    calls the application service `buy_item`, and returns a structured response.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BuyItemRequestSerializer

    @extend_schema(
        request=BuyItemRequestSerializer, responses=BuyItemResponseSerializer
    )
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = buy_item(
            user=request.user,
            item_code=serializer.validated_data["item_code"],
            quantity=serializer.validated_data["quantity"],
        )
        payload = {"success": True, "result": result}
        response_serializer = BuyItemResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)


class GetRodStoreListAPIView(GenericAPIView):
    serializer_class = GetRodListRequestSerializer

    @extend_schema(
        request=GetRodListRequestSerializer, responses=GetRodListResponseSerializer
    )
    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = get_rod_store_list()

        payload = {"success": True, "result": result}

        response_serializer = GetRodListResponseSerializer(payload)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class GetBaitStoreListAPIView(GenericAPIView):
    serializer_class = GetBaitListRequestSerializer

    extend_schema(
        request=GetBaitListRequestSerializer, responses=GetBaitListResponseSerializer
    )

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = get_bait_store_list()
        payload = {"success": True, "result": result}
        response_serializer = GetBaitListResponseSerializer(payload)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
