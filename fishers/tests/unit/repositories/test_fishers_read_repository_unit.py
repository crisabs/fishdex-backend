from django.db import DatabaseError
import pytest
from fishers.infrastructure.repositories.fishers_read_repository import (
    get_fisher_details_me_repository,
)
from unittest.mock import patch
from fishers.models import Fisher
from core.exceptions.domain import FisherNotFoundError
from core.exceptions.bd import RepositoryError


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="user1fromtest@user.com", password="user1fromtestuser1fromtest"
    )


@pytest.fixture
def fisher(user):
    return Fisher.objects.create(user=user, nickname="user1fromtest@user.com")


@pytest.mark.unit
@patch("fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get")
def test_get_fisher_details_me_respository_database_error_unit(
    mock_fisher_objects_get, user
):
    """
    GIVEN a user with an existing fisher profile
    WHEN a database error occur while fetching fisher details
    THEN raises RepositoryError
    """

    mock_fisher_objects_get.side_effect = DatabaseError()

    with pytest.raises(RepositoryError):
        get_fisher_details_me_repository(user=user)


@pytest.mark.unit
@patch("fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get")
def test_get_fisher_details_me_respository_raises_fisher_not_found_error_unit(
    mock_fisher_objects_get, user
):
    """
    GIVEN a user with an existing fisher profile
    WHEN a database error occur while fetching fisher details
    THEN raises FisherNotFoundError
    """

    mock_fisher_objects_get.side_effect = Fisher.DoesNotExist()

    with pytest.raises(FisherNotFoundError):
        get_fisher_details_me_repository(user=user)
