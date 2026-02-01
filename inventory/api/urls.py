from django.urls import path
from inventory.api.views import InventoryItemListView

app_name = "inventory"

urlpatterns = [path("items/", InventoryItemListView.as_view(), name="item-list")]
