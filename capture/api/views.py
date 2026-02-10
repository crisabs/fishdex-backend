from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from capture.domain.services.capture_fish_service import capture_fish_service
from capture.api.serializers.capture_fish_request_serializer import (
    CaptureFishRequestSerializer,
)
from capture.api.serializers.capture_fish_response_serializer import (
    CaptureFishResponseSerializer,
)


class CaptureFishAPIView(GenericAPIView):
    """
    API endpoint that handles fish capture attempts by an authenticated user,
    valiting input and returning the capture result.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CaptureFishRequestSerializer

    @extend_schema(
        request=CaptureFishRequestSerializer, responses=CaptureFishResponseSerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = capture_fish_service(
            user=request.user,
            rod_code=serializer.validated_data["used_rod"],
            bait_code=serializer.validated_data["used_bait"],
            fish_id=serializer.validated_data["fish_id"],
            fish_weight=serializer.validated_data["fish_weight"],
            fish_length=serializer.validated_data["fish_length"],
        )

        payload = {"success": True, "result": response}

        response_serializer = CaptureFishResponseSerializer(data=payload)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
