from typing import Tuple, cast
from rest_framework.test import APIClient
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.urls import reverse
import pytest
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_item_factory import FisherItemFactory
from inventory.models import FisherItem
from inventory.tests.factories.user_factory import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher_and_fisher_item(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser, FisherItem]:
    fisher = FisherFactory()
    fisherItem = FisherItemFactory(fisher=fisher)

    refresh = cast(RefreshToken, RefreshToken.for_user(user=fisher.user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return (api_client, fisher.user, fisherItem)


@pytest.fixture
def authenticated_user_without_fisher(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser]:
    user = UserFactory()

    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return (api_client, user)


@pytest.fixture
def unauthenticated_user(db):
    return UserFactory()


def test_intentory_item_list_api_returns_data(
    authenticated_user_with_fisher_and_fisher_item,
):
    """
    GIVEN an authenticated user and the inventory service returns an item list
    WHEN the inventory item list endpoint is requested
    THEN the API responds with HTTP 200 and the inventory items in the response body
    """

    client, _, fisherItem = authenticated_user_with_fisher_and_fisher_item
    expected_return_value = [
        {
            "item_code": fisherItem.item.code,
            "item_name": fisherItem.item.name,
            "quantity": fisherItem.quantity,
        },
    ]
    url = reverse("inventory:item-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"] == expected_return_value


def test_inventory_item_list_api_unauthenticated_user(api_client):
    """
    GIVEN an unauthenticated user
    WHEN the inventory item list endpoint is requested
    THEN the API responds with HTTP 401 unauthotized
    """

    url = reverse("inventory:item-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_inventory_item_list_api_returns_500_when_service_raises_fisher_not_found(
    authenticated_user_without_fisher,
):
    """
    GIVEN an authenticated user and the inventory service raises a FisherNotFoundError
    WHEN the inventory item list endpoint is requested
    THEN the API responds with HTTP 500 internal server error
    """

    url = reverse("inventory:item-list")
    client, _ = authenticated_user_without_fisher
    response = client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
