from fishers.api.serializers.fisher_me_response_serializer import (
    FisherMeResponseSerializer,
)


def test_fisher_me_response_serializer_success():
    data = {"nickname": "nickname", "level": 10}
    serializer = FisherMeResponseSerializer(data=data)
    assert serializer.is_valid() is True


def test_fisher_me_response_serializer_missing_nickname():
    data = {"level": 10}
    serializer = FisherMeResponseSerializer(data=data)
    assert serializer.is_valid() is False


def test_fisher_me_response_serializer_missing_level():
    data = {"nickname": "nickname"}
    serializer = FisherMeResponseSerializer(data=data)
    assert serializer.is_valid() is False
