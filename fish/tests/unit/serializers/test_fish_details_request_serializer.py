from fish.api.serializers.fish_details_request_serializer import (
    FishDetailsRequestSerializer,
)


def test_fish_details_request_serializer_success():
    payload = {"fish_id": 9}
    serializer = FishDetailsRequestSerializer(data=payload)
    assert serializer.is_valid()


def test_fish_details_request_serializer_missing_fish_id():
    payload = {}
    serializer = FishDetailsRequestSerializer(data=payload)
    assert not serializer.is_valid()


def test_fish_details_request_serializer_invalid_fish_id():
    payload = {"fish_id": -1}
    serializer = FishDetailsRequestSerializer(data=payload)
    assert not serializer.is_valid()
