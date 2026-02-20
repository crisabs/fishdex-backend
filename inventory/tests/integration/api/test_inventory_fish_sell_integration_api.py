from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from typing import cast
from fishers.models import Fisher
from inventory.models import FisherFish
from fish.models import Fish
from django.urls import reverse

import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher_and_fill_to_sell(django_user_model, api_client):
    """Fixture to create an authenticated user with
    a fisher and a fish in their inventory for testing the fish selling API endpoint."""
    user = django_user_model.objects.create_user(
        username="testuser@user.com", password="testuser"
    )
    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    fisher = Fisher.objects.create(user=user, nickname=user)
    fish = Fish.objects.get(fish_id=1)

    fisher_fish = FisherFish.objects.create(
        fisher=fisher, fish=fish, weight=12.1, length=1
    )

    return api_client, user, fisher, fisher_fish


class TestSellFishIntegrationSuccess:
    @pytest.mark.django_db
    def test_inventory_fish_sell_integration_ok_response(
        self, authenticated_user_with_fisher_and_fill_to_sell
    ):
        """
        GIVEN an authenticated user with a fisher and a fish in their inventory
        WHEN the user attempts to sell a fish through the inventory API
        THEN the API should return a successful response indicating the fish was sold
        and the user's inventory was updated accordingly.
        """
        url = reverse("inventory:fish_sell")
        client, _, fisher, fisher_fish = authenticated_user_with_fisher_and_fill_to_sell

        pk = fisher_fish.pk
        fish_id = (
            FisherFish.objects.filter(fisher=fisher)
            .select_related("fish")
            .values_list("fish__fish_id", flat=True)
            .first()
        )
        weight = fisher_fish.weight

        payload = {
            "pk": pk,
            "fish_id": fish_id,
            "total_weight": weight,
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
