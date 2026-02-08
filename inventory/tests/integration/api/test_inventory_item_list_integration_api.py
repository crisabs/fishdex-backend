from typing import Tuple, cast
from rest_framework.test import APIClient
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from unittest.mock import patch
from django.urls import reverse
import pytest

from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError


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
    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return (api_client, user)


@patch("inventory.api.views.get_inventory_item_list")
def test_intentory_item_list_api_returns_data(mock_service, authenticated_user):
    """
    GIVEN an authenticated user and the inventory service returns an item list
    WHEN the inventory item list endpoint is requested
    THEN the API responds with HTTP 200 and the inventory items in the response body
    """

    mock_service.return_value = [
        {"item_code": "ROD_BASIC", "item_name": "Basic Rod", "quantity": 13},
    ]
    url = reverse("inventory:item-list")
    client, user = authenticated_user
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"] == mock_service.return_value

    mock_service.assert_called_once_with(user=user)


def test_inventory_item_list_api_unauthenticated_user(api_client):
    """
    GIVEN an unauthenticated user
    WHEN the inventory item list endpoint is requested
    THEN the API responds with HTTP 401 unauthotized
    """

    url = reverse("inventory:item-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@patch("inventory.api.views.get_inventory_item_list")
def test_inventory_item_list_api_returns_500_when_service_raises_fisher_not_found_error(
    mock_service, authenticated_user
):
    """
    GIVEN an authenticated user and the inventory service raises a FisherNotFoundError
    WHEN the inventory item list endpoint is requested
    THEN the API responds with HTTP 500 internal server error
    """

    mock_service.side_effect = FisherNotFoundError()

    url = reverse("inventory:item-list")
    client, user = authenticated_user
    response = client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    mock_service.assert_called_once_with(user=user)


@patch("inventory.api.views.get_inventory_item_list")
def test_inventory_item_list_api_returns_500_when_service_raises_repository_error(
    mock_service, authenticated_user
):
    """
    GIVEN an authenticated user and the inventory service raises a RepositoryError
    WHEN the inventory item list endpoint is requested
    THEN the API responds with HTTP 500 internal server error
    """

    mock_service.side_effect = RepositoryError()

    url = reverse("inventory:item-list")
    client, user = authenticated_user
    response = client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    mock_service.assert_called_once_with(user=user)
