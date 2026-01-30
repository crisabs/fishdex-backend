from typing import Tuple, cast
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.urls import reverse
from fish.models import Fish
from django.contrib.auth.models import AbstractBaseUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(
    api_client, django_user_model
) -> Tuple[APIClient, AbstractBaseUser]:
    user = django_user_model.objects.create_user(
        username="user_for_test1@user.com",
        password="user_for_test1",
    )

    refresh = cast(RefreshToken, RefreshToken.for_user(user=user))
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, user


def test_fish_details_integration_api_success(authenticated_user):
    """
    GIVEN an authenticated user and a fish stored in the database
    WHEN the fish details endpoint is requested with a valid fish_id
    THEN the API returns a successful response with the fish details.
    """

    test_fish_id = 99
    test_fish_name = "Test Largemouth Bass"
    Fish.objects.create(
        fish_id=test_fish_id,
        name=test_fish_name,
        description="A popular sport fish with powerful strikes.",
        habitat="LAKE",
        rarity="RARE",
        base_weight=3.5,
        base_price=30.0,
    )

    url = reverse("fish:get_fish_details")
    client, _ = authenticated_user
    payload = {"fish_id": test_fish_id}
    response = client.get(url, payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"]["name"] == test_fish_name
