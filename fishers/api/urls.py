from django.urls import path
from fishers.api.views import (
    FisherMeAPIView,
    FisherNicknameAPIView,
    FisherChangeZoneAPIView,
)

app_name = "fishers"

urlpatterns = [
    path("me/", FisherMeAPIView.as_view(), name="details_me"),
    path("nickname/", FisherNicknameAPIView.as_view(), name="nickname"),
    path("change-zone/", FisherChangeZoneAPIView.as_view(), name="change_zone"),
]
