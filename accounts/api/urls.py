from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.api.views import AccountRegisterAPIView, AccountLogoutAPIView

app_name = "accounts"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("register/", AccountRegisterAPIView.as_view(), name="register"),
    path("logout/", AccountLogoutAPIView.as_view(), name="logout"),
]
