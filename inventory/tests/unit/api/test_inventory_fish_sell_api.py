from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser@user.com",
        password="testpassword",
    )
    api_client.force_authenticate(user=user)
    return api_client


@patch("inventory.api.views.sell_fish")
def test_sell_fish_success(mock_sell_fish, authenticated_api_client):
    """
    GIVEN a valid request to sell a fish
    WHEN the request is made to the inventory fish sell endpoint
    THEN the fish is sold successfully and a 200 OK response is returned
    """

    mock_sell_fish.return_value = {
        "code": "OK",
    }
    url = reverse("inventory:fish_sell")
    client = authenticated_api_client
    payload = {
        "fish_id": 1,
        "total_weight": 2,
        "pk": 10,
    }
    response = client.post(url, data=payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["code"] == mock_sell_fish.return_value["code"]


def test_sell_fish_unauthenticated(api_client):
    """
    GIVEN an unauthenticated request to sell a fish
    WHEN the request is made to the inventory fish sell endpoint
    THEN a 401 Unauthorized response is returned
    """
    url = reverse("inventory:fish_sell")
    client = api_client
    payload = {
        "fish_id": 1,
        "total_weight": 2,
        "pk": 10,
    }
    response = client.post(url, data=payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
