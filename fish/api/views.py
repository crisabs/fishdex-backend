from venv import logger
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from fish.domain.services.fish_service import get_fish_list, get_fish_details
from fish.api.serializers.fish_list_response_serializer import (
    FishListResponseSerializer,
)
from fish.api.serializers.fish_details_request_serializer import (
    FishDetailsRequestSerializer,
)
from fish.api.serializers.fish_details_response_serializer import (
    FishDetailsResponseSerializer,
)


class FishListAPIView(GenericAPIView):
    """
    Retrieve the list of available fishes.

    Authentication is required.
    Returns a successful response containing a list of fishes.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=FishListResponseSerializer(many=True),
        description="Returns the list of all available fishes.",
    )
    def get(self, request):
        result = get_fish_list()
        payload = {"success": True, "results": result}

        response_serializer = FishListResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)
        return Response(
            response_serializer.validated_data,
            status=status.HTTP_200_OK,
        )


class FishDetailsAPIView(GenericAPIView):
    """
    Retrieve the details of a specific fish.

    Authentication is required.
    The fish is identified by its fish_id
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FishDetailsRequestSerializer

    @extend_schema(
        request=FishDetailsRequestSerializer,
        responses=FishDetailsResponseSerializer,
        description="Returns the details of a fish given its fish_id.",
    )
    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = get_fish_details(serializer.validated_data["fish_id"])
        payload = {"success": True, "result": result}

        response_serializer = FishDetailsResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
