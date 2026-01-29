from typing import Tuple
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from typing import cast
from django.urls import reverse

from fish.models import Fish


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, django_user_model) -> Tuple[APIClient, object]:
    user = django_user_model.objects.create_user(
        username="user_test_jwt@user.com", password="user_test_jwt"
    )

    refresh = RefreshToken.for_user(user=user)
    access_token = str(cast(RefreshToken, refresh).access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client, user


def test_fish_list_integration_api_success(authenticated_user):
    """
    GIVEN an authenticated user and an existing fish stored in the database
    WHEN the user requests the fish list endpoint
    THEN the API returns a successful response including the created fish
    """

    Fish.objects.create(
        fish_id=299,
        name="Salmon_test",
        description="A strong migratory fish known for swimming upstream.",
        habitat="RIVER",
        rarity="COMMON",
        base_weight=3.0,
        base_price=15.0,
    )

    url = reverse("fish:get_list_fishes")
    client, _ = authenticated_user
    response = client.get(url, format="json")
    assert "success" in response.data
    assert "results" in response.data

    assert response.status_code == status.HTTP_200_OK

    assert response.data["success"] is True
    assert isinstance(response.data["results"], list)

    created_fish = next(
        (fish for fish in response.data["results"] if fish["name"] == "Salmon_test"),
        None,
    )
    assert created_fish is not None
    assert created_fish["fish_id"] == 299
    assert created_fish["habitat"] == "RIVER"
    assert created_fish["rarity"] == "COMMON"
