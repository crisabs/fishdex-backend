from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from typing import cast
from fishers.models import Fisher


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher_profile(django_user_model, api_client):
    """
    GIVEN an authenticated user with an associated Fisher profile
    WHEN the spawned fish capture endpoint is requested
    THEN the API returns HTTP 200 with a successful response
    AND the result contains a valid spawned fish ID as an integer.
    """

    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )

    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    Fisher.objects.create(user=user, nickname=user)
    return api_client, user


def test_capture_spawned_fish_integration_api_return_data(
    authenticated_user_with_fisher_profile,
):
    """
    GIVEN an unauthenticated user
    WHEN the spawned fish capture endpoint is requested
    THEN the API returns HTTP 401 (Unauthorized).
    """

    client, _ = authenticated_user_with_fisher_profile
    url = reverse("capture:spawned_fish")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"] in (1, 2, 3, 4, 5)


def test_capture_spawned_fish_integration_api_unauthenticated_user(api_client):
    url = reverse("capture:spawned_fish")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
