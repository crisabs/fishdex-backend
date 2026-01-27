from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from django.urls import reverse
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_from_test1@user.com", password="user_from_test1"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("fish.api.views.get_fish_list")
def test_fish_list_returns_data(mock_get_fish_list, authenticated_user):
    """
    GIVEN an authenticated user
    WHEN requesting fishes list
    THEN returns status 200 and fishes list data
    """
    mock_get_fish_list.return_value = [
        {
            "id": 9,
            "name": "Salmon",
            "fish_id": 1,
            "description": "A strong migratory fish known for swimming upstream.",
            "habitat": "RIVER",
            "rarity": "COMMON",
            "base_weight": 3.0,
            "base_price": 15.0,
        },
    ]

    client, user = authenticated_user
    url = reverse("fish:get_list_fishes")
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["data"] == mock_get_fish_list.return_value


def test_fish_list_user_not_authenticated(api_client):
    """
    GIVEN an unauthenticated user
    WHEN accesing the endpoint
    THEN returns 401 Unauthorized
    """
    url = reverse("fish:get_list_fishes")
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
