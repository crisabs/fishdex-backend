from django.urls import path
from fish.api.views import FishListAPIView

app_name = "fish"

urlpatterns = [
    path("get-list-fishes/", FishListAPIView.as_view(), name="get_list_fishes")
]
