import pytest
from django.contrib.auth.models import User
from accounts.infrastructure.repositories.accounts_write_repository import (
    create_account_repository,
)

from fishers.models import Fisher


@pytest.mark.django_db
def test_create_account_repository():
    """
    GIVEN an email and a password
    WHEN create_account_repository is called
    THEN a User and a Fisher are created in the db
    """
    # GIVEN
    data = {"email": "user1@example.com", "password": "passworduser1"}

    # WHEN
    user = create_account_repository(email=data["email"], password=data["password"])

    # THEN
    db_user = User.objects.get(username=data["email"])
    assert db_user == user

    fisher = Fisher.objects.get(user=user)
    assert fisher.nickname == data["email"]
