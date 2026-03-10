import pytest
from core.exceptions.domain import (
    FisherNotFoundError,
    InvalidZoneError,
    NotEnoughCoinsError,
)
from fishers.domain.services.fishers_service import set_fisher_zone
from fishers.tests.factories.fisher_factory import FisherFactory
from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher_valid(db):
    fisher = FisherFactory(coins=1500)
    return fisher.user


@pytest.fixture
def user_without_fisher(db):
    return UserFactory()


@pytest.fixture
def user_with_fisher_invalid(db):
    fisher = FisherFactory(coins=50)
    return fisher.user


class TestSetFishersZoneSuccess:
    def test_fishers_zone_returns_data(self, user_with_fisher_valid):
        """
        GIVEN a user with a corresponding Fisher profile and enough coins
        WHEN set_fisher_zone is called with that user and a valid new zone
        THEN it returns a confirmation message with the new zone"""
        new_zone = "LAKE"
        result = set_fisher_zone(user=user_with_fisher_valid, new_zone=new_zone)
        assert result == {"code": "ZONE_CHANGED", "new_zone": new_zone}


class TestSetFishersZoneErrors:
    def test_fishers_zone_raises_fisher_not_enough_coins(
        self, user_with_fisher_invalid
    ):
        """
        GIVEN a user with a corresponding Fisher profile but insufficient coins
        WHEN set_fisher_zone is called with that user and a valid new zone
        THEN it raises a NotEnoughCoinsError"""
        new_zone = "LAKE"
        with pytest.raises(NotEnoughCoinsError):
            set_fisher_zone(user=user_with_fisher_invalid, new_zone=new_zone)

    def test_fishers_zone_raises_invalid_zone_error(self, user_with_fisher_valid):
        """
        GIVEN a user with a corresponding Fisher profile and enough coins
        WHEN set_fisher_zone is called with that user and an invalid new zone
        THEN it raises an InvalidZoneError
        """
        new_zone = "VOLCANO"
        with pytest.raises(InvalidZoneError):
            set_fisher_zone(user=user_with_fisher_valid, new_zone=new_zone)

    def test_fishers_zone_raises_fisher_not_found_error(self, user_without_fisher):
        """
        GIVEN a user without a corresponding Fisher profile
        WHEN set_fisher_zone is called with that user and a valid new zone
        THEN it raises a FisherNotFoundError
        """
        new_zone = "LAKE"
        with pytest.raises(FisherNotFoundError):
            set_fisher_zone(user=user_without_fisher, new_zone=new_zone)
