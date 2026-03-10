from typing import Tuple

import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.infrastructure.repositories.fishers_write_repository import (
    set_fisher_nickname_repository,
)
from fishers.tests.factories.fisher_factory import FisherFactory
from django.contrib.auth.models import AbstractBaseUser
from fishers.models import Fisher
from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher(db) -> Tuple[AbstractBaseUser, Fisher]:
    fisher = FisherFactory()
    return fisher.user, fisher


@pytest.fixture
def user_without_fisher(db) -> AbstractBaseUser:
    return UserFactory()


class TestFisherNicknameRepositorySuccess:
    def test_set_fisher_nickname_repository_returns_confirmation_message(
        self, user_with_fisher
    ):
        """
        GIVEN a user with an associated fisher profile in the database
        WHEN updating the fisher's nickname using the write repository
        THEN it returns a confirmation message with the new nickname
        """
        user, fisher = user_with_fisher
        result = set_fisher_nickname_repository(user=user, nickname="new_nickname")
        fisher.refresh_from_db()
        assert result == f"Fisher nickname updated to {fisher.nickname}"
        assert fisher.nickname == "new_nickname"


class TestFisherNicknameRepositoryErrors:
    def test_set_fisher_nickname_repository_raises_fisher_not_found(
        self, user_without_fisher
    ):
        """
        GIVEN a user without an associated fisher profile in the database
        WHEN updating the fisher's nickname using the write repository
        THEN it raises a FisherNotFoundError
        """
        with pytest.raises(FisherNotFoundError):
            set_fisher_nickname_repository(
                user=user_without_fisher, nickname="new_nickname"
            )

    def test_set_fisher_nickname_repository_raises_repository_error(
        self, user_with_fisher
    ):
        """
        GIVEN a user with an associated fisher profile in the database
        WHEN updating the fisher's nickname using the write repository
        with an invalid nickname
        THEN it raises a RepositoryError"""
        invalid_nickname = "x" * 200
        user, _ = user_with_fisher
        with pytest.raises(RepositoryError):
            set_fisher_nickname_repository(user=user, nickname=invalid_nickname)
