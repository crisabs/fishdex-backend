from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.urls import reverse
from typing import cast
import pytest

from fish.models import Fish
from fishers.models import Fisher
from inventory.models import FisherFish


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(django_user_model, api_client):
    user = django_user_model.objects.create_user(
        username="usertest@user.com", password="usertest"
    )
    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, user


@pytest.fixture
def unauthenticated_user(django_user_model):
    return django_user_model.objects.create_user(
        username="usertest@user.com", password="usertest"
    )


class TestInventoryFishDescriptionIntegraionSuccess:
    def test_inventory_description_integration_api_returns_data(
        self, authenticated_user
    ):
        """
        GIVEN a valid request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain the updated description and a success status
        """
        url = reverse("inventory:fisher_fish_description")
        client, user = authenticated_user

        fish = Fish.objects.get(fish_id=1)
        fisher = Fisher.objects.create(user=user, nickname=user)
        fisherFish = FisherFish.objects.create(
            fisher=fisher, fish=fish, weight=1, length=1
        )

        payload = {"pk": fisherFish.pk, "description": "A new description"}
        response = client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK


class TestInventoryFishDescriptionIntegraionErrors:
    def test_inventory_description_integration_api_invalid_pk(self, authenticated_user):
        """
        GIVEN an invalid primary key in the request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain an error message and a 500 status code
        """
        url = reverse("inventory:fisher_fish_description")
        client, _ = authenticated_user
        payload = {"pk": 455, "description": "A new description"}
        response = client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_inventory_description_integration_api_invalid_description(
        self, authenticated_user
    ):
        """
        GIVEN an invalid description in the request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain an error message and a 400 status code
        """
        url = reverse("inventory:fisher_fish_description")
        client, user = authenticated_user

        fish = Fish.objects.get(fish_id=1)
        fisher = Fisher.objects.create(user=user, nickname=user)
        fisherFish = FisherFish.objects.create(
            fisher=fisher, fish=fish, weight=1, length=1
        )

        payload = {
            "pk": fisherFish.pk,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris"
            " nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
            "Excepteur sint occaecat cupidatat non proident, "
            "sunt in culpa qui officia deserunt mollit anim id est laborum.",
        }
        response = client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inventory_description_integration_api_unauthenticated(
        self, unauthenticated_user, api_client
    ):
        """GIVEN an unauthenticated user making a request to the inventory description endpoint
        WHEN the request is made
        THEN the response should contain an error message and a 401 status code
        """
        url = reverse("inventory:fisher_fish_description")

        fish = Fish.objects.get(fish_id=1)
        fisher = Fisher.objects.create(
            user=unauthenticated_user, nickname=unauthenticated_user
        )
        fisherFish = FisherFish.objects.create(
            fisher=fisher, fish=fish, weight=1, length=1
        )

        payload = {"pk": fisherFish.pk, "description": "A new description"}
        response = api_client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
