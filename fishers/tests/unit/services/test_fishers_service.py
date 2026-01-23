from unittest.mock import patch
import pytest
from fishers.domain.services.fishers_service import get_fisher_detail_me
from core.exceptions.domain import FisherNotFoundError
from core.exceptions.bd import RepositoryError
from fishers.domain.services.fishers_service import set_fisher_nickname


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="user_from_test1@user.com", password="userfromtest1userfromtest1"
    )


@patch("fishers.domain.services.fishers_service.get_fisher_details_me_repository")
def test_get_fisher_details_sucess(mock_get_fisher_details_me_repository, user):
    """
    GIVEN a user with an existing fisher profile
    WHEN retrieving fisher details from the service
    THEN thr fisher profile data is returned
    """

    mock_get_fisher_details_me_repository.return_value = {
        "nickname": "user_from_test1@user.com",
        "level": 25,
        "coins": 50,
        "current_zone": "Lake",
    }

    result = get_fisher_detail_me(user=user)

    assert result["nickname"] == "user_from_test1@user.com"


@pytest.mark.django_db
def test_get_fisher_details_fisher_not_found_error(user):
    """
    GIVEN a user without an associated fisher profile
    WHEN retrieving fisher details from the service
    THEN a FisherNotFoundError is raised
    """

    with pytest.raises(FisherNotFoundError):
        get_fisher_detail_me(user=user)


@pytest.mark.django_db
@patch("fishers.domain.services.fishers_service.get_fisher_details_me_repository")
def test_get_fisher_details_repository_error(mock_repo, user):
    """
    GIVEN a valid user
    WHEN the repository raises a RepositoryError
    THEN the service propagates the RepositoryError
    """

    mock_repo.side_effect = RepositoryError

    with pytest.raises(RepositoryError):
        get_fisher_detail_me(user=user)


@patch("fishers.domain.services.fishers_service.set_fisher_nickname_repository")
def test_set_fisher_nickname_success(mock_repository, user):
    """
    GIVEN a valid user with a fisher profile
    WHEN updating the fisher nickname via the service
    THEN a confirmation message is returned
    """

    nickname = "OldFisher"
    mock_repository.return_value = "Fisher nickname updated to {nickname}"
    result = set_fisher_nickname(user=user, nickname=nickname)
    assert result == "Fisher nickname updated to {nickname}"

    mock_repository.assert_called_once_with(user=user, nickname=nickname)


@patch("fishers.domain.services.fishers_service.set_fisher_nickname_repository")
def test_set_fisher_nickname_fisher_not_found_error(mock_repository, user):
    """
    GIVEN a valid user without an associated fisher profile
    WHEN the service attempts to update the fisher nickname
    THEN a FisherNotFoundError is raised
    """
    nickname = "OldFisher"
    mock_repository.side_effect = FisherNotFoundError
    with pytest.raises(FisherNotFoundError):
        set_fisher_nickname(user, nickname=nickname)


@patch("fishers.domain.services.fishers_service.set_fisher_nickname_repository")
def test_set_fisher_nickname_repository_error(mock_repository, user):
    """
    GIVEN a valid user with an associated fisher profile
    WHEN then service updates the fisher nickname and a repository error occurs
    THEN a RepositoryError is raised
    """
    nickname = "OldFisher"
    mock_repository.side_effect = RepositoryError
    with pytest.raises(RepositoryError):
        set_fisher_nickname(user, nickname=nickname)
