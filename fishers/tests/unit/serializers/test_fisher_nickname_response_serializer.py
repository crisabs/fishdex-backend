from fishers.api.serializers.fisher_nickname_response_serializer import (
    FisherNicknameResponseSerializer,
)


def test_fisher_nickname_response_serializer_success():
    response_data = {"success": True, "message": "Fisher nickname updated to "}
    serializer = FisherNicknameResponseSerializer(data=response_data)
    assert serializer.is_valid()


def test_fisher_nickname_response_serializer_message_empty():
    response_data = {"success": True, "message": ""}
    serializer = FisherNicknameResponseSerializer(data=response_data)
    assert not serializer.is_valid()
