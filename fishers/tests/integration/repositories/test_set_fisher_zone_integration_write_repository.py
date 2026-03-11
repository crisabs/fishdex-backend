from typing import Tuple

import pytest
from core.exceptions.domain import FisherNotFoundError
from fishers.tests.factories.fisher_factory import FisherFactory
from fishers.infrastructure.repositories.fishers_write_repository import (
    set_fisher_zone_repository,
)
from django.contrib.auth.models import AbstractBaseUser
from fishers.models import Fisher
from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher(db) -> Tuple[AbstractBaseUser, Fisher]:
    fisher = FisherFactory(coins=800)
    return fisher.user, fisher


@pytest.fixture
def user_without_fisher(db) -> AbstractBaseUser:
    return UserFactory()


class TestSetFisherZoneSuccess:
    def test_set_fisher_zone_returns_new_zone(self, user_with_fisher):
        """
        Given a user with a fisher, when setting a new zone,
        then the fisher's zone is updated and a confirmation message is returned
        """
        new_zone = "OCEAN"
        user, fisher = user_with_fisher
        result = set_fisher_zone_repository(user=user, new_zone=new_zone, zone_cost=100)
        fisher.refresh_from_db()
        assert result == f"Fisher is now in the zone: {new_zone}"
        assert fisher.current_zone == new_zone


class TestSetFisherZoneErrors:
    def test_set_fisher_zone_raises_fisher_not_found(self, user_without_fisher):
        """
        Given a user without a fisher, when setting a new zone,
        then it raises a FisherNotFoundError
        """
        new_zone = "OCEAN"
        with pytest.raises(FisherNotFoundError):
            set_fisher_zone_repository(
                user=user_without_fisher, new_zone=new_zone, zone_cost=100
            )
