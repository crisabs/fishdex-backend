from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(django_user_model, api_client):
    user = django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("inventory.api.views.get_inventory_fish_list")
def test_inventory_fish_list_api_returns_data(mock_service, authenticated_user):
    """
    GIVEN An authenticated user and the inventory fish service mocked
    to return a valid fish list.
    WHEN The authenticated user sends a GET request to the inventory fish list endpoit.
    THEN The API responds with HTTP 200, a successful flag,
    and the expected list of fishes serialized according to the API contract.
    """
    mock_service.return_value = [
        {
            "fish_name": "Salmon",
            "price": 4,
            "weight": "0.30",
            "caught_at": "2026-02-10T05:52:57.267600Z",
            "rarity": "COMMON",
        },
    ]
    url = reverse("inventory:fishes-list")
    client, _ = authenticated_user
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"] == mock_service.return_value


@patch("inventory.api.views.get_inventory_fish_list")
def test_inventory_fish_list_api_unauthenticated_user(mock_service, api_client):
    """
    GIVEN An unauthenticated client and  the inventory fish service mocked.
    WHEN the client sends a GET request to the inventory fish list endpoint.
    THEN the API responds with HTTP 401 Unauthorized.
    """
    mock_service.return_value = [
        {
            "fish_name": "Salmon",
            "price": 4,
            "weight": "0.30",
            "caught_at": "2026-02-10T05:52:57.267600Z",
            "rarity": "COMMON",
        },
    ]
    url = reverse("inventory:fishes-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
