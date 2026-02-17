from typing import Tuple
from pytest import fixture
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from django.contrib.auth.models import AbstractBaseUser


@fixture
def api_client():
    return APIClient()


@fixture
def authenticated_user(
    api_client, django_user_model
) -> Tuple[APIClient, AbstractBaseUser]:
    user = django_user_model.objects.create_user(
        username="user1@user.com", password="user1user1"
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@patch("fishers.api.views.get_fisher_detail_me")
def test_fisher_me_authenticated_user_returns_fisher_data(
    mock_get_fisher_detail_me, authenticated_user
):
    """
    GIVEN an authenticated user
    WHEN requesting fisher details
    THEN returns status 200 and fisher data
    """

    mock_get_fisher_detail_me.return_value = {
        "nickname": "Old Fisher",
        "level": 33,
        "coins": 35,
        "current_zone": "River",
    }

    # GIVEN
    client, user = authenticated_user

    # WHEN
    url = reverse("fishers:details_me")
    response = client.get(url)

    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["data"]["nickname"] == "Old Fisher"

    mock_get_fisher_detail_me.assert_called_once_with(user=user)


def test_fisher_me_user_not_authenticated(api_client):
    """
    GIVEN an unauthenticated request
    WHEN accesing the endpoint
    THEN returns 401 Unauthorized
    """
    # GIVEN / WHEN
    url = reverse("fishers:details_me")
    response = api_client.get(url)

    # THEN
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "credentials" in response.data["detail"].lower()
