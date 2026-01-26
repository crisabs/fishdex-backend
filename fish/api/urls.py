from django.urls import path
from fish.api.views import FishListAPIView

urlpatterns = [
    path("get-list-fishes/", FishListAPIView.as_view(), name="get_list_fishes")
]
