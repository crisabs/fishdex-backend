from capture.api.serializers.capture_fish_request_serializer import (
    CaptureFishRequestSerializer,
)


def test_capture_fish_request_serializer_success():
    payload = {
        "used_rod": "ROD_BASIC",
        "used_bait": "BAIT_BASIC",
        "fish_id": 1,
        "fish_weight": 0.3,
        "fish_length": 1.2,
    }
    serializer = CaptureFishRequestSerializer(data=payload)
    assert serializer.is_valid() is True


def test_capture_fish_request_serializer_missing_params():
    payload = {
        "fish_id": 1,
        "fish_weight": 0.3,
        "fish_length": 1.2,
    }
    serializer = CaptureFishRequestSerializer(data=payload)
    assert not serializer.is_valid()
