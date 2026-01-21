from rest_framework.exceptions import ValidationError
import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from accounts.domain.services.accounts_service import logout_account


@pytest.mark.django_db
def test_account_service_logout_success():
    User = get_user_model()
    user = User.objects.create_user(username="user1@user.com", password="user1user1")

    refresh = RefreshToken.for_user(user=user)
    logout_account(str(refresh))


def test_account_service_logout_without_token():
    with pytest.raises(ValidationError) as exc:
        logout_account("")
    assert "refresh token required" in str(exc.value)


def test_account_service_logout_invalid_token():
    with pytest.raises(ValidationError) as exc:
        logout_account("this-is-not-a-jwt")
    assert "invalid or expired refresh token" in str(exc)
