from django.urls import path
from store.api.views import BuyItemAPIView

app_name = "store"

urlpatterns = [
    path("buy-item/", BuyItemAPIView.as_view(), name="buy_item"),
]
