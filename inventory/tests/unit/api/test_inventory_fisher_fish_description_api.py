from rest_framework.test import APIClient
from rest_framework import status
import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="testpassword"
    )
    api_client.force_authenticate(user=user)
    return api_client


@patch("inventory.api.views.set_description_fisher_fish")
def test_set_description_fisher_fish_success_returns_data(
    mock_service, authenticated_api_client
):
    """
    GIVEN a valid request to set the description of a fisher fish inventory record
    WHEN the request is processed
    THEN the service function should be called with
    the correct parameters and a successful response should be returned
    """
    mock_service.return_value = {"success": True}

    url = reverse("inventory:fisher_fish_description")
    client = authenticated_api_client

    payload = {"pk": 1, "description": "A custom inventory fish description"}
    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True


def test_set_description_fisher_fish_unauthenticated_returns_401(api_client):
    """
    GIVEN an unauthenticated request to set the description
    of a fisher fish inventory record
    WHEN the request is processed
    THEN a 401 Unauthorized response should be returned"""
    url = reverse("inventory:fisher_fish_description")
    client = api_client

    payload = {"pk": 1, "description": "A custom inventory fish description"}
    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_set_description_fisher_fish_invalid_data_returns_400(authenticated_api_client):
    """
    GIVEN an authenticated request with invalid data to set the description
    of a fisher fish inventory record
    WHEN the request is processed
    THEN a 400 Bad Request response should be returned
    """
    url = reverse("inventory:fisher_fish_description")
    client = authenticated_api_client

    payload = {"pk": "invalid_pk", "description": 123}
    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
