from typing import cast
from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from fishers.models import Fisher
from typing import Tuple
from django.contrib.auth.models import AbstractBaseUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(
    api_client, django_user_model
) -> Tuple[APIClient, AbstractBaseUser]:
    """
    Creates a user with a fisher profile and authenticates
    the client with a JWT access token.
    Returns the APIClient and the user instance.
    """
    user = django_user_model.objects.create_user(
        username="user_jwt@test.com", password="strongpassword123"
    )

    Fisher.objects.create(
        user=user, nickname="JWT Fisher", level=10, coins=200, current_zone="Lake"
    )

    refresh = cast(RefreshToken, RefreshToken.for_user(user))
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, user


@pytest.mark.django_db
def test_fisher_me_with_valid_jwt_returns_fisher_data(authenticated_user):
    """
    GIVEN a user with JWT
    WHEN requesting /api/fishers/me/
    THEN returns 200 OK and fisher data
    """

    # --- GIVEN ---
    client, user = authenticated_user

    url = reverse("fishers:details_me")

    # --- WHEN ---
    response = client.get(url)

    # --- THEN ---
    assert response.status_code == 200
    assert response.data["success"] is True
    assert response.data["data"] == {
        "nickname": "JWT Fisher",
        "level": 10,
        "coins": 200,
        "current_zone": "Lake",
    }
