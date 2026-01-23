from typing import cast
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from fishers.models import Fisher
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_jwttest1@user.com", password="user_jwttest1user_test1"
    )

    Fisher.objects.create(user=user, nickname=user.username)

    refresh = RefreshToken.for_user(user)
    access_token = str(cast(RefreshToken, refresh).access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return api_client, user


def test_fisher_nickname_success(authenticated_user):
    client, user = authenticated_user
    url = reverse("fishers:nickname")
    payload = {"nickname": "nickname"}

    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert (
        response.data["message"] == "Fisher nickname updated to user_jwttest1@user.com"
    )
