from typing import Tuple
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import AbstractBaseUser
from unittest.mock import patch
from django.urls import reverse
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(
    api_client, django_user_model
) -> Tuple[APIClient, AbstractBaseUser]:
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("inventory.api.views.get_inventory_item_list")
def test_inventory_item_list_api_returns_data(mock_service, authenticated_user):
    """
    Given an authenticated user and a mocked inventory service returning items
    When the inventoy item list endpoint is requested
    Then the API responds with HTTP 200 and the expected payload
    """
    mock_service.return_value = [
        {"item_code": "ROD_BASIC", "item_name": "Basic Rod", "quantity": 13},
    ]

    client, _ = authenticated_user
    url = reverse("inventory:item-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"] == mock_service.return_value


def test_inventory_item_list_api_unauthenticated_user_error(api_client):
    """
    Given an unauthenticated client
    When the inventoty item list endpoint is requested
    Then the API responds with HTTP 401 Unauthorized
    """
    url = reverse("inventory:item-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
