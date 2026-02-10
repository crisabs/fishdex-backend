from typing import Tuple
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from django.urls import reverse
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(
    api_client, django_user_model
) -> Tuple[APIClient, AbstractBaseUser]:
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("capture.api.views.capture_fish_service")
def test_capture_fish_api_returns_data(mock_service, authenticated_user):
    """
    GIVEN an authenticated user and a valid fish capture request
    WHEN the capture endpoint is called
    THEN it returns a successful response with the capture result
    """

    mock_service.return_value = {"captured": False, "message": "The fish escaped"}
    url = reverse("capture:capture_fish")
    client, user = authenticated_user
    payload = {
        "used_rod": "ROD_BASIC",
        "used_bait": "BAIT_BASIC",
        "fish_id": 1,
        "fish_weight": 0.3,
        "fish_length": 1.2,
    }
    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"] == mock_service.return_value

    mock_service.assert_called_once_with(
        user=user,
        rod_code=payload["used_rod"],
        bait_code=payload["used_bait"],
        fish_id=payload["fish_id"],
        fish_weight=payload["fish_weight"],
        fish_length=payload["fish_length"],
    )


def test_capture_fish_api_returns_unauthenticated(api_client):
    """
    GIVEN an unauthenticated user
    WHEN the capture endpoint is called
    THEN it returns an unauthorized response
    """

    url = reverse("capture:capture_fish")
    payload = {
        "used_rod": "ROD_BASIC",
        "used_bait": "BAIT_BASIC",
        "fish_id": 1,
        "fish_weight": 0.3,
        "fish_length": 1.2,
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
