from typing import Tuple, cast
from rest_framework.test import APIClient
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.urls import reverse
import pytest
from inventory.models import FisherFish
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory
from inventory.tests.factories.user_factory import UserFactory

# from core.exceptions.bd import RepositoryError
# from core.exceptions.domain import FisherNotFoundError


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher_profile_and_fisher_fish(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser, FisherFish]:
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)

    refresh = cast(RefreshToken, RefreshToken.for_user(user=fisher.user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return api_client, fisher.user, fisherFish


@pytest.fixture
def authenticated_user_without_fisher_profile(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser]:
    user = UserFactory()

    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return api_client, user


@pytest.fixture
def unauthenticated_user_with_fisher_profile_and_fisher_fish(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser, FisherFish]:
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)

    return api_client, fisher.user, fisherFish


class TestInventoryFishListSuccess:

    def test_inventory_fish_list_api_returns_data(
        self,
        authenticated_user_with_fisher_profile_and_fisher_fish,
    ):
        """
        GIVEN an authenticated user with a fisher profile and at least one fisher fish
        WHEN the inventory fish list endpoint is requested
        THEN the API responds with HTTP 200 OK and returns
        the fisher fish data in the expected format
        """

        url = reverse("inventory:fishes-list")
        client, _, fisherFish = authenticated_user_with_fisher_profile_and_fisher_fish
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

        assert response.data["success"] is True
        assert response.data["result"][0]["fish_name"] == fisherFish.fish.name


class TestInventoryFishListErrors:
    def test_inventory_fish_list_api_unauthenticated_user(
        self,
        unauthenticated_user_with_fisher_profile_and_fisher_fish,
    ):
        """
        GIVEN an unauthenticated user
        WHEN the inventory fish list endpoint is requested
        THEN the API responds with HTTP 401 unauthotized
        """
        api_client, _, _ = unauthenticated_user_with_fisher_profile_and_fisher_fish
        url = reverse("inventory:fishes-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_inventory_fish_list_api_internal_server_error(
        self,
        authenticated_user_without_fisher_profile,
    ):
        """
        GIVEN an authenticated user without a fisher profile
        WHEN the inventory fish list endpoint is requested
        THEN the API responds with HTTP 500 Internal Server Error
         due to the unhandled FisherNotFoundError exception
         raised in the service layer when trying to retrieve fisher fish data
         for a user without a fisher profile
        """
        api_client, _ = authenticated_user_without_fisher_profile
        url = reverse("inventory:fishes-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
