from django.urls import path
from fish.api.views import FishListAPIView, FishDetailsAPIView

app_name = "fish"

urlpatterns = [
    path("get-list-fishes/", FishListAPIView.as_view(), name="get_list_fishes"),
    path("get-fish-details/", FishDetailsAPIView.as_view(), name="get_fish_details"),
]
