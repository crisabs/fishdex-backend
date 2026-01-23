import pytest
from fishers.infrastructure.repositories.fishers_write_repository import (
    set_fisher_nickname_repository,
)
from fishers.models import Fisher
from core.exceptions.domain import FisherNotFoundError
from core.exceptions.bd import RepositoryError
from unittest.mock import patch


@pytest.fixture
def user_with_fisher_profile(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test_repository@user.com",
        password="user_test_repository",
    )

    Fisher.objects.create(user=user, nickname=user.username)
    return user


@pytest.fixture
def user_without_fisher_profile(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test_repository@user.com",
        password="user_test_repository",
    )


@pytest.mark.django_db
def test_set_fisher_nickname_repository_success(user_with_fisher_profile):
    nickname = "nickname"
    result = set_fisher_nickname_repository(
        user=user_with_fisher_profile, nickname=nickname
    )
    assert result == f"Fisher nickname updated to {nickname}"


def test_set_fisher_nickname_repository_fisher_does_not_exist(
    user_without_fisher_profile,
):
    with pytest.raises(FisherNotFoundError):
        set_fisher_nickname_repository(
            user=user_without_fisher_profile, nickname="nickname"
        )


@patch("fishers.infrastructure.repositories.fishers_write_repository.Fisher.save")
def test_set_fisher_nickname_repository_database_error(
    mock_fisher_save, user_with_fisher_profile
):
    mock_fisher_save.side_effect = RepositoryError
    with pytest.raises(RepositoryError):
        set_fisher_nickname_repository(
            user=user_with_fisher_profile, nickname="nickname"
        )
