from django.urls import path
from inventory.api.views import InventoryItemListView, InventoryFishListView

app_name = "inventory"

urlpatterns = [
    path("items/", InventoryItemListView.as_view(), name="item-list"),
    path("fishes/", InventoryFishListView.as_view(), name="fishes-list"),
]
