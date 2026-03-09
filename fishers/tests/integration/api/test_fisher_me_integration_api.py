from typing import cast
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Tuple
from django.contrib.auth.models import AbstractBaseUser

from fishers.models import Fisher
from fishers.tests.factories.fisher_factory import FisherFactory
from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser, Fisher]:
    """
    Creates a user with a fisher profile and authenticates
    the client with a JWT access token.
    Returns the APIClient and the user instance.
    """
    fisher = FisherFactory()

    refresh = cast(RefreshToken, RefreshToken.for_user(fisher.user))
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, fisher.user, fisher


@pytest.fixture
def authenticated_user_without_fisher_profile(db, api_client):
    user = UserFactory()
    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, user


class TestFisherMeSuccess:
    def test_fisher_me_with_valid_jwt_returns_fisher_data(
        self,
        authenticated_user_with_fisher,
    ):
        """
        GIVEN a user with JWT
        WHEN requesting /api/fishers/me/
        THEN returns 200 OK and fisher data
        """

        client, user, fisher = authenticated_user_with_fisher
        url = reverse("fishers:details_me")
        response = client.get(url)

        assert response.status_code == 200
        assert response.data["success"] is True
        assert response.data["result"] == {
            "nickname": fisher.nickname,
            "level": fisher.level,
            "coins": fisher.coins,
            "current_zone": fisher.current_zone,
        }


class TestFisherMeErrors:
    def test_fisher_me_user_unauthenticated_error(self, api_client):
        """
        GIVEN an unauthenticated user
        WHEN requesting /api/fishers/me/
        THEN returns 401 Unauthorized"""
        url = reverse("fishers:details_me")
        result = api_client.get(url)
        assert result.status_code == status.HTTP_401_UNAUTHORIZED

    def test_fisher_me_raises_fisher_not_found(
        self,
        authenticated_user_without_fisher_profile,
    ):
        """
        GIVEN an authenticated user without a fisher profile
        WHEN requesting /api/fishers/me/
        THEN returns 404 Not Found with appropriate error message
        """
        url = reverse("fishers:details_me")
        client, _ = authenticated_user_without_fisher_profile
        result = client.get(url)

        assert result.status_code == status.HTTP_404_NOT_FOUND
