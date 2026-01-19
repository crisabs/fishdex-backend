from accounts.api.serializers.account_register_response_serializer import (
    AccountRegisterResponseSerializer,
)


def test_accounts_register_response_serializer_valid():
    data = {"success": True, "data": "OK"}
    serializer = AccountRegisterResponseSerializer(data=data)
    assert serializer.is_valid() is True
