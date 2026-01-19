from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from accounts.api.serializers.account_register_serializer import (
    AccountRegisterSerializer,
)
from accounts.api.serializers.account_register_response_serializer import (
    AccountRegisterResponseSerializer,
)
from accounts.api.serializers.account_logout_serializer import AccountLogoutSerializer

from rest_framework import permissions
from accounts.domain.services.accounts_service import register_account, logout_account
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

import logging

logger = logging.getLogger(__name__)


class AccountRegisterAPIView(GenericAPIView):
    serializer_class = AccountRegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=AccountRegisterSerializer, responses=AccountRegisterResponseSerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = register_account(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return Response(
            {"success": True, "data": result["data"]}, status=status.HTTP_200_OK
        )


class AccountLogoutAPIView(GenericAPIView):
    serializer_class = AccountLogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=AccountLogoutSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logout_account(refresh_token=serializer.validated_data["refresh"])
        return Response(status=status.HTTP_204_NO_CONTENT)
