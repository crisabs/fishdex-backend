from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.urls import reverse
from typing import cast
import pytest
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory
from inventory.tests.factories.fisher_factory import FisherFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher_profile_and_fisher_fish(db, api_client):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)

    refresh = cast(RefreshToken, RefreshToken.for_user(user=fisher.user))
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, fisher.user, fisherFish


@pytest.fixture
def unauthenticated_user_with_fisher_profile_and_fisher_fish(db):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)
    return fisher.user, fisherFish


class TestInventoryFishDescriptionIntegraionSuccess:
    def test_inventory_description_integration_api_returns_data(
        self, authenticated_user_with_fisher_profile_and_fisher_fish
    ):
        """
        GIVEN a valid request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain the updated description and a success status
        """
        url = reverse("inventory:fisher_fish_description")
        client, _, fisherFish = authenticated_user_with_fisher_profile_and_fisher_fish

        payload = {"pk": fisherFish.pk, "description": "A new description"}
        response = client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK


class TestInventoryFishDescriptionIntegraionErrors:
    def test_inventory_description_integration_api_invalid_pk(
        self, authenticated_user_with_fisher_profile_and_fisher_fish
    ):
        """
        GIVEN an invalid primary key in the request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain an error message and a 500 status code
        """
        url = reverse("inventory:fisher_fish_description")
        client, _, _ = authenticated_user_with_fisher_profile_and_fisher_fish
        payload = {"pk": 455, "description": "A new description"}
        response = client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_inventory_description_integration_api_invalid_description(
        self, authenticated_user_with_fisher_profile_and_fisher_fish
    ):
        """
        GIVEN an invalid description in the request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain an error message and a 400 status code
        """
        url = reverse("inventory:fisher_fish_description")
        client, _, fisherFish = authenticated_user_with_fisher_profile_and_fisher_fish

        invalid_description = "x" * 300

        payload = {
            "pk": fisherFish.pk,
            "description": invalid_description,
        }
        response = client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inventory_description_integration_api_unauthenticated(
        self, unauthenticated_user_with_fisher_profile_and_fisher_fish, api_client
    ):
        """
        GIVEN an unauthenticated user making a request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain an error message and a 401 status code
        """
        url = reverse("inventory:fisher_fish_description")

        user, fisherFish = unauthenticated_user_with_fisher_profile_and_fisher_fish

        payload = {"pk": fisherFish.pk, "description": "A new description"}
        response = api_client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
