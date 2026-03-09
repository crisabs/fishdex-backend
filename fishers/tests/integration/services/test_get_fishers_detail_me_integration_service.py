from typing import Tuple
from core.exceptions.domain import FisherNotFoundError
from fishers.domain.services.fishers_service import get_fisher_detail_me
import pytest

from fishers.models import Fisher
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


class TestFishersDetailMeSuccess:
    def test_get_fisher_detail_me_returns_data(self, user_with_fisher):
        """
        GIVEN a user with a corresponding Fisher profile
        WHEN get_fisher_detail_me is called with that user
        THEN it returns a dictionary containing
        the fisher's nickname, level, coins, and current zone
        """
        user, fisher = user_with_fisher
        result = get_fisher_detail_me(user=user)

        assert result["nickname"] == fisher.nickname
        assert result["level"] == fisher.level
        assert result["coins"] == fisher.coins
        assert result["current_zone"] == fisher.current_zone


class TestFishersDetailErrors:

    def test_get_fisher_detail_me_raises_fisher_not_found(self, user_without_fisher):
        """
        GIVEN a user without a corresponding Fisher profile
        WHEN get_fisher_detail_me is called with that user
        THEN it raises a FisherNotFoundError
        """
        with pytest.raises(FisherNotFoundError):
            get_fisher_detail_me(user_without_fisher)
