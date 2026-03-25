from django.urls import path
from store.api.views import (
    BuyItemAPIView,
    GetRodStoreListAPIView,
    GetBaitStoreListAPIView,
)

app_name = "store"

urlpatterns = [
    path("buy-item/", BuyItemAPIView.as_view(), name="buy_item"),
    path(
        "get-rod-store-list/",
        GetRodStoreListAPIView.as_view(),
        name="get_rod_store_list",
    ),
    path(
        "get-bait-store-list/",
        GetBaitStoreListAPIView.as_view(),
        name="get_bait_store_list",
    ),
]
