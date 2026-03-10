from typing import Tuple

import pytest
from core.exceptions.domain import FisherNotFoundError
from fishers.infrastructure.repositories.fishers_read_repository import get_fisher_coins
from fishers.tests.factories.fisher_factory import FisherFactory
from fishers.tests.factories.user_factory import UserFactory
from django.contrib.auth.models import AbstractBaseUser
from fishers.models import Fisher


@pytest.fixture
def user_with_fisher(db) -> Tuple[AbstractBaseUser, Fisher]:
    fisher = FisherFactory(coins=200)
    return fisher.user, fisher


@pytest.fixture
def user_without_fisher(db):
    return UserFactory()


class TestGetFisherCoinsSuccess:
    def test_get_fisher_coins_return_coins(self, user_with_fisher):
        """
        GIVEN a user with an associated fisher profile in the database
        WHEN fetching the fisher's coins from the read repository
        THEN returns the number of coins the fisher has
        """
        user, fisher = user_with_fisher
        result = get_fisher_coins(user=user)
        assert result == fisher.coins


class TestGetFisherCoinsErrors:
    def test_get_fisher_coins_raise_fisher_not_found(self, user_without_fisher):
        """
        GIVEN a user without an associated fisher profile in the database
        WHEN fetching the fisher's coins from the read repository
        THEN raises a FisherNotFoundError
        """
        with pytest.raises(FisherNotFoundError):
            get_fisher_coins(user=user_without_fisher)
