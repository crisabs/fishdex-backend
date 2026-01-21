import pytest
from unittest.mock import patch
from accounts.domain.services.accounts_service import register_account
from django.contrib.auth.models import User


@pytest.mark.django_db
@patch("accounts.domain.services.accounts_service.create_account_repository")
def test_register_account_returns_data(mock_create_account_repository):
    mock_create_account_repository.return_value = User(username="user1@example.com")
    """
    GIVEN a email and a password
    THEN create a user and a fisher models
    THEN save in the db and return a successull message
    """

    # GIVEN
    data = {"email": "user1@example.com", "password": "passworduser1"}

    # WHEN
    result = register_account(email=data["email"], password=data["password"])

    # THEN
    mock_create_account_repository.assert_called_once_with(
        email=data["email"], password=data["password"]
    )

    assert result == {"data": "OK"}
