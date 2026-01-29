from venv import logger
import pytest
from rest_framework.test import APIClient
from typing import Tuple
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, django_user_model) -> Tuple[APIClient, object]:
    user = django_user_model.objects.create(
        username="user_test_details@user.com", password="user_test_details"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("fish.api.views.get_fish_details")
def test_fish_details_api_returns_data(mock_service, authenticated_user):

    mock_service.return_value = {
        "fish_id": 9,
        "name": "Largemouth Bass",
        "description": "A popular sport fish with powerful strikes.",
        "habitat": "LAKE",
        "rarity": "RARE",
        "base_weight": 3.5,
        "base_price": 30.0,
    }

    url = reverse("fish:get_fish_details")
    client, _ = authenticated_user
    payload = {"fish_id": 9}
    response = client.get(url, data=payload, format="json")

    logger.debug("response.data %s", response.data)

    assert response.data["success"] is True
    assert response.status_code == status.HTTP_200_OK
    assert response.data["result"]["name"] == "Largemouth Bass"


def test_fish_details_api_unauthenticated_user(api_client):
    url = reverse("fish:get_fish_details")
    payload = {"fish_id": 9}
    response = api_client.get(url, data=payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
