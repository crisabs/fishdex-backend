from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from store.domain.store_service import buy_item
from drf_spectacular.utils import extend_schema
from store.api.serializers.buy_item_request_serializer import BuyItemRequestSerializer
from store.api.serializers.buy_item_response_serializer import BuyItemResponseSerializer


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
