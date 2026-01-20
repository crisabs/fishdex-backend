from django.urls import path
from fishers.api.views import FisherMeAPIView

app_name = "fishers"

urlpatterns = [path("me/", FisherMeAPIView.as_view(), name="details-me")]
