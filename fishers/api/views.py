from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework import permissions
from rest_framework.response import Response
from core.exceptions.domain import FisherNotFoundError
from fishers.api.serializers.fisher_change_zone_request_serializer import (
    FisherChangeZoneRequestSerializer,
)
from fishers.api.serializers.fisher_change_zone_response_serializer import (
    FisherChangeZoneResponseSerializer,
)
from drf_spectacular.utils import extend_schema
from fishers.api.serializers.fishers_fisher_me_request_serializer import (
    FishersFisherMeRequestSerializer,
)
from fishers.api.serializers.fishers_fisher_me_response_serializer import (
    FishersFisherMeResponseSerializer,
)
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
from rest_framework.exceptions import NotFound


class FisherMeAPIView(GenericAPIView):
    """
    GIVEN an authenticated user
    WHEN the user requests their fisher details
    THEN the API returns a 200 OK response with the user's
    nickname, level, coins, and current zone
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FishersFisherMeRequestSerializer

    @extend_schema(
        request=FishersFisherMeRequestSerializer,
        responses=FishersFisherMeResponseSerializer,
    )
    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        try:
            result = get_fisher_detail_me(user=request.user)
        except FisherNotFoundError as exc:
            raise NotFound(detail=exc.default_detail)

        payload = {"success": True, "result": result}
        response_serializer = FishersFisherMeResponseSerializer(payload)

        return Response(
            response_serializer.data,
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
        try:
            response_service = set_fisher_nickname(user=request.user, nickname=nickname)
        except FisherNotFoundError as exc:
            raise NotFound(exc.default_detail)

        payload = {"success": True, "message": response_service}
        response_serializer = FisherNicknameResponseSerializer(payload)

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
