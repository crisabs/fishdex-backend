from fishers.api.serializers.fisher_nickname_request_serializer import (
    FisherNicknameRequestSerializer,
)


def test_fisher_nickname_request_serializer_success():
    request_data = {"nickname": "TheOldFisherMan"}
    serializer = FisherNicknameRequestSerializer(data=request_data)
    assert serializer.is_valid()
    assert serializer.validated_data["nickname"] == "TheOldFisherMan"


def test_fisher_nickname_request_serializer_invalid_nickname():
    request_data = {"nickname": "TheOldFisherMan SELECT ALL WHERE ="}
    serializer = FisherNicknameRequestSerializer(data=request_data)
    assert not serializer.is_valid()
    assert "nickname" in serializer.errors


def test_fisher_nickname_request_serializer_empty_nickname():
    request_data = {"nickname": ""}
    serializer = FisherNicknameRequestSerializer(data=request_data)
    assert not serializer.is_valid()
    assert "nickname" in serializer.errors
