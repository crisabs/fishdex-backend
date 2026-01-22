from django.urls import path
from fishers.api.views import FisherMeAPIView, FisherNicknameAPIView

app_name = "fishers"

urlpatterns = [
    path("me/", FisherMeAPIView.as_view(), name="details-me"),
    path("nickname/", FisherNicknameAPIView.as_view(), name="nickname"),
]
