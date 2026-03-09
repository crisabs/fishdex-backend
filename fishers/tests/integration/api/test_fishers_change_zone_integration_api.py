from typing import Tuple, cast

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import AbstractBaseUser
from fishers.tests.factories.fisher_factory import FisherFactory
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status

from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser]:
    fisher = FisherFactory(coins=800)

    refresh = cast(RefreshToken, RefreshToken.for_user(user=fisher.user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, fisher.user


@pytest.fixture
def authenticated_user_without_fisher(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser]:
    user = UserFactory()

    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, user


class TestFishersChangeZoneSuccess:
    def test_fishers_change_zone_returns_data(self, authenticated_user_with_fisher):
        """
        GIVEN an authenticated user with a fisher profile
        WHEN the user sends a PATCH request to change their fishing zone
        THEN the API validates the input, updates the fishing zone,
        and returns a 200 OK response with the new zone and a success code"""
        client, _ = authenticated_user_with_fisher
        url = reverse("fishers:change_zone")
        payload = {"new_zone": "LAKE"}
        result = client.patch(url, payload, format="json")
        assert result.status_code == status.HTTP_200_OK
        assert result.data["code"] == "ZONE_CHANGED"
        assert result.data["new_zone"] == payload["new_zone"]


class TestFishersChangeZoneErrors:
    def test_fishers_change_zone_unauthenticated_user_error(self, api_client):
        """
        GIVEN an unauthenticated user
        WHEN the user sends a PATCH request to change their fishing zone
        THEN the API returns a 401 Unauthorized response indicating authentication is required
        """
        url = reverse("fishers:change_zone")
        payload = {"new_zone": "LAKE"}
        result = api_client.patch(url, payload, format="json")
        assert result.status_code == status.HTTP_401_UNAUTHORIZED

    def test_fishers_change_zone_raises_fisher_not_found_errir(
        self, authenticated_user_without_fisher
    ):
        """
        GIVEN an authenticated user without a fisher profile
        WHEN the user sends a PATCH request to change their fishing zone
        THEN the API returns a 404 Not Found response indicating the fisher profile is missing
        """
        client, _ = authenticated_user_without_fisher
        url = reverse("fishers:change_zone")
        payload = {"new_zone": "LAKE"}
        result = client.patch(url, payload, format="json")
        assert result.status_code == status.HTTP_404_NOT_FOUND
