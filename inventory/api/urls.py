from django.urls import path
from inventory.api.views import (
    InventoryFishSellAPIView,
    InventoryFisherFishDescriptionView,
    InventoryItemListView,
    InventoryFishListView,
)

app_name = "inventory"

urlpatterns = [
    path("items/", InventoryItemListView.as_view(), name="item-list"),
    path("fishes/", InventoryFishListView.as_view(), name="fishes-list"),
    path("fish-sell/", InventoryFishSellAPIView.as_view(), name="fish_sell"),
    path(
        "fisher-fish-description/",
        InventoryFisherFishDescriptionView.as_view(),
        name="fisher_fish_description",
    ),
]
