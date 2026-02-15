from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from django.urls import reverse
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("capture.api.views.get_spawned_fish")
def test_capture_spawned_fish_api_return_data(mock_service, authenticated_user):
    """
    GIVEN an authenticated user and the fish spawning service returning a spawned fish
    WHEN the user requests the spawned fish capture endpoint
    THEN the API returns a successful response with the spawned fish data
    """
    mock_service.return_value = "Salmon"
    client, _ = authenticated_user
    url = reverse("capture:spawned_fish")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["result"] == mock_service.return_value


def test_capture_spawned_fish_api_unauthenticated_user(api_client):
    """
    GIVEN an unauthenticated client
    WHEN the spawned fish capture endpoint is requested
    THEN the API responds with an unauthorized error
    """
    url = reverse("capture:spawned_fish")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
