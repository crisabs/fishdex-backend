from pytest import fixture
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from core.exceptions.bd import RepositoryError


@fixture
def api_client():
    return APIClient()


@fixture
def authenticated_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="user1@user.com", password="user1user1"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("fishers.api.views.set_fisher_nickname")
def test_fisher_nickname_success(mock_service, authenticated_user):
    """
    GIVEN an authenticated user
    WHEN the nickname update endpoint is called
    THEN it returns a confirmation message with HTTP 200
    """

    payload = {"nickname": "OldFisher"}
    mock_service.return_value = f"Fisher nickname updated to {payload['nickname']}"
    url = reverse("fishers:nickname")
    client, user = authenticated_user

    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["message"] == f"Fisher nickname updated to {payload['nickname']}"
    )

    mock_service.assert_called_once_with(user=user, nickname=payload["nickname"])


def test_fisher_nickname_invalid_payload(authenticated_user):
    """
    GIVEN an authenticated user
    WHEN payload is invalid
    THEN the API returns HTTP 400
    """
    client, user = authenticated_user
    payload = {"nickname": ""}
    url = reverse("fishers:nickname")

    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@patch("fishers.api.views.set_fisher_nickname")
def test_fisher_nickname_internal_server_error(mock_service, authenticated_user):
    """
    GIVEN an authenticated user
    WHEN the nickname update service raises a repository error
    THEN the API returns HTTP 500
    """

    client, user = authenticated_user
    payload = {"nickname": "nickname"}
    url = reverse("fishers:nickname")

    mock_service.side_effect = RepositoryError

    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_fisher_nickname_unauthenticated_user(api_client):
    """
    GIVEN an user without authentication
    WHEN calling the nickname update endpoint
    THEN returns HTTP 401 Unauthorized
    """
    payload = {"nickname": "nickname"}
    url = reverse("fishers:nickname")

    response = api_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
