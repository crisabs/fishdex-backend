from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from typing import cast
from django.urls import reverse

from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher_and_fisher_fish_to_sell(db, api_client):
    """
    Fixture to create an authenticated user with
    a fisher and a fish in their inventory for testing the fish selling API endpoint.
    """
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)

    refresh = cast(RefreshToken, RefreshToken.for_user(user=fisher.user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return api_client, fisher.user, fisherFish


class TestSellFishIntegrationSuccess:
    def test_inventory_fish_sell_integration_ok_response(
        self, authenticated_user_with_fisher_and_fisher_fish_to_sell
    ):
        """
        GIVEN an authenticated user with a fisher and a fish in their inventory
        WHEN the user attempts to sell a fish through the inventory API
        THEN the API should return a successful response indicating the fish was sold
        and the user's inventory was updated accordingly.
        """
        url = reverse("inventory:fish_sell")
        client, _, fisherFish = authenticated_user_with_fisher_and_fisher_fish_to_sell

        payload = {
            "pk": fisherFish.pk,
            "fish_id": fisherFish.fish.fish_id,
            "total_weight": fisherFish.weight,
        }

        response = client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == "OK"


class TestSellFishIntegrationErrors:
    def test_inventory_fish_sell_integration_api_unauthenticated_user_error(
        self, api_client
    ):
        """
        GIVEN an unauthenticated user
        WHEN the user attempts to sell a fish through the inventory API
        THEN the API should return an unauthorized error response
        indicating that authentication is required.
        """
        url = reverse("inventory:fish_sell")
        payload = {
            "pk": 1,
            "fish_id": 1,
            "total_weight": 12.1,
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_inventory_fish_sell_integration_api_missing_weight(
        self, authenticated_user_with_fisher_and_fisher_fish_to_sell
    ):
        url = reverse("inventory:fish_sell")
        payload = {
            "pk": 1,
            "fish_id": 1,
        }
        api_client, _, _ = authenticated_user_with_fisher_and_fisher_fish_to_sell
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inventory_fish_sell_integration_api_missing_fish_id(
        self, authenticated_user_with_fisher_and_fisher_fish_to_sell
    ):
        url = reverse("inventory:fish_sell")
        payload = {
            "pk": 1,
            "total_weight": 12.1,
        }
        api_client, _, _ = authenticated_user_with_fisher_and_fisher_fish_to_sell
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inventory_fish_sell_integration_api_missing_fish_pk(
        self, authenticated_user_with_fisher_and_fisher_fish_to_sell
    ):
        url = reverse("inventory:fish_sell")
        payload = {
            "fish_id": 1,
            "total_weight": 12.1,
        }
        api_client, _, _ = authenticated_user_with_fisher_and_fisher_fish_to_sell
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inventory_fish_sell_integration_api_invalid_fish_id(
        self, authenticated_user_with_fisher_and_fisher_fish_to_sell
    ):
        """
        GIVEN an authenticated user with a fisher and a fish in their inventory
        WHEN the user attempts to sell a fish with an invalid fish_id through the inventory API
        THEN the API should return an error response
        indicating that the specified fish could not be found."""
        url = reverse("inventory:fish_sell")
        payload = {
            "pk": 1,
            "fish_id": -1,
            "total_weight": 12.1,
        }
        api_client, _, _ = authenticated_user_with_fisher_and_fisher_fish_to_sell
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inventory_fish_sell_integration_api_invalid_pk(
        self, authenticated_user_with_fisher_and_fisher_fish_to_sell
    ):
        """
        GIVEN an authenticated user with a fisher and a fish in their inventory
        WHEN the user attempts to sell a fish with an invalid pk through the inventory API
        THEN the API should return an error response
        indicating that the specified fish could not be found.
        """
        url = reverse("inventory:fish_sell")
        payload = {
            "pk": 999,
            "fish_id": 1,
            "total_weight": 12.1,
        }
        api_client, _, _ = authenticated_user_with_fisher_and_fisher_fish_to_sell
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
