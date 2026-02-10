from capture.api.serializers.capture_fish_response_serializer import (
    CaptureFishResponseSerializer,
)


def test_capture_fish_response_serializer_success():
    payload = {
        "success": True,
        "result": {"captured": False, "message": "The fish escaped"},
    }
    serializer = CaptureFishResponseSerializer(data=payload)
    assert serializer.is_valid() is True


def test_capture_fish_response_serializer_missing_result():
    payload = {
        "success": True,
    }
    serializer = CaptureFishResponseSerializer(data=payload)
    assert not serializer.is_valid()
