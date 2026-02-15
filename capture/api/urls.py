from django.urls import path
from capture.api.views import CaptureFishAPIView, CaptureSpawnedFish

app_name = "capture"

urlpatterns = [
    path("capture/", CaptureFishAPIView.as_view(), name="capture_fish"),
    path("spawned-fish/", CaptureSpawnedFish.as_view(), name="spawned_fish"),
]
