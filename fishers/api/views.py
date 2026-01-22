from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from fishers.api.serializers.fisher_me_response_serializer import (
    FisherMeResponseSerializer,
)
from drf_spectacular.utils import extend_schema
from fishers.domain.services.fishers_service import (
    get_fisher_detail_me,
    set_fisher_nickname,
)
from fishers.api.serializers.fisher_nickname_serializer import (
    FisherNicknameRequestSerializer,
)
from fishers.api.serializers.fisher_nickname_response_serializer import (
    FisherNicknameResponseSerializer,
)


class FisherMeAPIView(GenericAPIView):
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
        response_service = set_fisher_nickname(nickname=nickname)

        response_serializer = FisherNicknameResponseSerializer(
            data={"success": True, "message": response_service}
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
