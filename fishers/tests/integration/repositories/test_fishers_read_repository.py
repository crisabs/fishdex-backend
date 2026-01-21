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


@pytest.mark.django_db
def test_get_fisher_details_me_repository_success(user, fisher):
    """
    GIVEN a user that has an associated fisher profile in the database
    WHEN fetching fisher details from the read repository
    THEN returns the fisher data mapped as a dictionary
    """
    result = get_fisher_details_me_repository(user=user)

    assert result == {
        "nickname": "user1fromtest@user.com",
        "level": 1,
        "coins": 100,
        "current_zone": "River",
    }


def test_get_fisher_details_me_repository_fisher_not_found(user):
    """
    GIVEN a user without an associated fisher profile in the database
    WHEN fetching fishers details from the repository
    THEN raises FisherNotFoundError
    """
    with pytest.raises(FisherNotFoundError):
        get_fisher_details_me_repository(user=user)


@patch("fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get")
def test_get_fisher_details_me_respository_database_error(
    mock_fisher_objects_get, user, fisher
):
    """
    GIVEN a user with an existing fisher profile
    WHEN a database error occura while fetching fisher details
    THEN raises RepositoryError
    """

    mock_fisher_objects_get.side_effect = RepositoryError

    with pytest.raises(RepositoryError):
        get_fisher_details_me_repository(user=user)
