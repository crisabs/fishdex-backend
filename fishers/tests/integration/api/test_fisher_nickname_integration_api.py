from typing import cast
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Tuple
from django.contrib.auth.models import AbstractBaseUser

from fishers.tests.factories.fisher_factory import FisherFactory
from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user_with_fisher(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser]:
    fisher = FisherFactory()

    refresh = RefreshToken.for_user(fisher.user)
    access_token = str(cast(RefreshToken, refresh).access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return api_client, fisher.user


@pytest.fixture
def authenticated_user_without_fisher(
    db, api_client
) -> Tuple[APIClient, AbstractBaseUser]:
    user = UserFactory(username="usertest@test.com")

    refresh = RefreshToken.for_user(user)
    access_token = str(cast(RefreshToken, refresh).access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return api_client, user


class TestFisherNicknameSucess:
    def test_fisher_nickname_success(self, authenticated_user_with_fisher):
        """
        GIVEN an authenticated user with a fisher profile
        WHEN the user sends a PATCH request to update their nickname
        THEN the API validates the input, updates the nickname,
        and returns a 200 OK response with a success message"""
        client, _ = authenticated_user_with_fisher
        url = reverse("fishers:nickname")
        payload = {"nickname": "nickname"}

        response = client.patch(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Fisher nickname updated to nickname"


class TestFisherNicknameErrors:
    def test_fisher_nickname_unauthenticated_user(self, api_client):
        """
        GIVEN an unauthenticated user
        WHEN the user sends a PATCH request to update their nickname
        THEN the API returns a 401 Unauthorized response"""
        url = reverse("fishers:nickname")
        payload = {"nickname": "nickname"}
        response = api_client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_fisher_nickname_raises_fisher_not_found(
        self, authenticated_user_without_fisher
    ):
        """
        GIVEN an authenticated user without a fisher profile
        WHEN the user sends a PATCH request to update their nickname
        THEN the API returns a 404 Not Found response
        """
        client, _ = authenticated_user_without_fisher
        url = reverse("fishers:nickname")
        payload = {"nickname": "nickname"}
        response = client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
