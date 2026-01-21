import pytest
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()


# False user for testing
@pytest.fixture
def authenticated_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="user1@user.com", password="user1user1"
    )
    api_client.force_authenticate(user=user)
    return api_client


# Valid logout test case
@patch("accounts.api.views.logout_account")
def test_accounts_logout(mock_logout_account, authenticated_user):
    client = authenticated_user
    mock_logout_account.return_value = None

    url = reverse("accounts:logout")

    payload = {"refresh": "dadjkadkdsaoidashdkasd"}
    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_logout_account.assert_called_once_with(refresh_token=payload["refresh"])
