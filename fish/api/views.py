from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from fish.domain.services.fish_service import get_fish_list
from fish.api.serializers.fish_list_response_serializer import (
    FishListResponseSerializer,
)


class FishListAPIView(GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=FishListResponseSerializer(many=True))
    def get(self, request):
        result = get_fish_list()
        payload = {"success": True, "results": result}

        response_serializer = FishListResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)
        return Response(
            response_serializer.validated_data,
            status=status.HTTP_200_OK,
        )
