from typing import Tuple
import pytest
from fishers.infrastructure.repositories.fishers_read_repository import (
    get_fisher_details_me_repository,
)
from fishers.models import Fisher
from core.exceptions.domain import FisherNotFoundError
from fishers.tests.factories.fisher_factory import FisherFactory
from django.contrib.auth.models import AbstractBaseUser
from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher(db) -> Tuple[AbstractBaseUser, Fisher]:
    fisher = FisherFactory()
    return fisher.user, fisher


@pytest.fixture
def user_without_fisher(db) -> AbstractBaseUser:
    return UserFactory()


class TestFisherDetailsSuccess:
    def test_get_fisher_details_me_repository_success(self, user_with_fisher):
        """
        GIVEN a user that has an associated fisher profile in the database
        WHEN fetching fisher details from the read repository
        THEN returns the fisher data mapped as a dictionary
        """
        user, fisher = user_with_fisher
        result = get_fisher_details_me_repository(user=user)

        assert result == {
            "nickname": fisher.nickname,
            "level": fisher.level,
            "coins": fisher.coins,
            "current_zone": fisher.current_zone,
        }


class TestFisherDetailsErrors:
    def test_get_fisher_details_me_repository_fisher_not_found(
        self, user_without_fisher
    ):
        """
        GIVEN a user without an associated fisher profile in the database
        WHEN fetching fishers details from the repository
        THEN raises FisherNotFoundError
        """
        with pytest.raises(FisherNotFoundError):
            get_fisher_details_me_repository(user=user_without_fisher)
