from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from fishers.api.serializers.fisher_change_zone_request_serializer import (
    FisherChangeZoneRequestSerializer,
)
from fishers.api.serializers.fisher_change_zone_response_serializer import (
    FisherChangeZoneResponseSerializer,
)
from fishers.api.serializers.fisher_me_response_serializer import (
    FisherMeResponseSerializer,
)
from drf_spectacular.utils import extend_schema
from fishers.domain.services.fishers_service import (
    get_fisher_detail_me,
    set_fisher_nickname,
    set_fisher_zone,
)
from fishers.api.serializers.fisher_nickname_request_serializer import (
    FisherNicknameRequestSerializer,
)
from fishers.api.serializers.fisher_nickname_response_serializer import (
    FisherNicknameResponseSerializer,
)


class FisherMeAPIView(GenericAPIView):
    """
    GIVEN an authenticated user
    WHEN the user requests their fisher details
    THEN the API returns a 200 OK response with the user's
    nickname, level, coins, and current zone
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FisherMeResponseSerializer

    @extend_schema(responses=FisherMeResponseSerializer)
    def get(self, request):
        result = get_fisher_detail_me(user=request.user)
        return Response(
            {"success": True, "data": result},
            status=status.HTTP_200_OK,
        )


class FisherNicknameAPIView(GenericAPIView):
    """
    GIVEN an authenticated user with a valid nickname
    WHEN the user sends a PATCH request to update their nickname
    THEN the API validates the input, updates the nickname,
    and returns a 200 OK response with a success message
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FisherNicknameRequestSerializer

    @extend_schema(
        request=FisherNicknameRequestSerializer,
        responses=FisherNicknameResponseSerializer,
    )
    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nickname = serializer.validated_data["nickname"]
        response_service = set_fisher_nickname(user=request.user, nickname=nickname)

        response_serializer = FisherNicknameResponseSerializer(
            data={"success": True, "message": response_service}
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class FisherChangeZoneAPIView(GenericAPIView):
    """
    GIVEN an authenticated user with a current fishing zone and a valid request payload
    containing a new zone
    WHEN the user sends a PATCH request to change their fishing zone
    THEN the API validates the requets, calls set_fisher_zone to update the zone,
    and returns a 200 OK response with the new zone if successful
    or raises an appropriate exception
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FisherChangeZoneRequestSerializer

    @extend_schema(
        request=FisherChangeZoneRequestSerializer,
        responses=FisherChangeZoneResponseSerializer,
    )
    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = set_fisher_zone(
            request.user, new_zone=serializer.validated_data["new_zone"]
        )

        serializer_response = FisherChangeZoneResponseSerializer(result)

        return Response(serializer_response.data, status=status.HTTP_200_OK)
