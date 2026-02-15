from capture.api.serializers.capture_spawned_fish_response_serializer import (
    CaptureSpawnedFishResponseSerializer,
)
from typing import cast


def test_capture_spawned_fish_response_serializer_success():
    payload = {"success": True, "result": "Salmon"}
    serializer = CaptureSpawnedFishResponseSerializer(payload)
    data = cast(dict, serializer.data)
    assert data["success"] is True
    assert data["result"] == "Salmon"


def test_capture_spawned_fish_response_serializer_error_requires_result():
    payload = {"success": True}
    serializer = CaptureSpawnedFishResponseSerializer(data=payload)
    assert not serializer.is_valid()
    assert "result" in serializer.errors
