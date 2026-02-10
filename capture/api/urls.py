from django.urls import path
from capture.api.views import CaptureFishAPIView

app_name = "capture"

urlpatterns = [path("capture/", CaptureFishAPIView.as_view(), name="capture_fish")]
