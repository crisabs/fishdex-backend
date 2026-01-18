import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
@patch("accounts.api.views.register_account")
def test_accounts_register_returns_data(mock_register_account, api_client):
    mock_register_account.return_value = {"data": "OK"}
    payload = {"email": "email@email.com", "password": "password123_#"}
    response = api_client.post(reverse("accounts:register"), payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["data"] == "OK"
    mock_register_account.assert_called_once_with(
        email=payload["email"], password=payload["password"]
    )
