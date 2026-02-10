from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from typing import cast
from fish import api
from fishers.models import Fisher
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )

    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return api_client, user


def test_capture_fish_integration_api_returns_data(authenticated_user):
    """
    GIVEN an authenticated user with an associated Fisher profile,
    WHEN the user sends a valid capture fish request to the API,
    THEN the API responds with HTTP 200 and a successful result.
    """

    client, user = authenticated_user

    Fisher.objects.create(user=user, nickname=user)

    url = reverse("capture:capture_fish")
    payload = {
        "used_rod": "ROD_BASIC",
        "used_bait": "BAIT_BASIC",
        "fish_id": 1,
        "fish_weight": 0.3,
        "fish_length": 1.2,
    }
    response = client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True


def test_capture_fish_integration_api_unauthenticated_user(
    api_client, django_user_model
):
    """
    GIVEN a user with an associated Fisher profile but no authentication credentials,
    WHEN a capture fish request is sent to the API,
    THEN the API responds with HTTP 401 Unauthorized.
    """
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )

    Fisher.objects.create(user=user, nickname=user)

    url = reverse("capture:capture_fish")
    payload = {
        "used_rod": "ROD_BASIC",
        "used_bait": "BAIT_BASIC",
        "fish_id": 1,
        "fish_weight": 0.3,
        "fish_length": 1.2,
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
