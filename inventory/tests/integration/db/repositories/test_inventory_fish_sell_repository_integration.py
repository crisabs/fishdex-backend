import pytest
from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from inventory.infrastructure.repositories.inventory_write_repository import (
    sell_fish_repository,
)

from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory
from inventory.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher_and_fisher_fish(db):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)
    return fisher.user, fisherFish


@pytest.fixture
def user_without_fisher_profile(db):
    return UserFactory()


class TestFishSellRepositoryIntegrationSuccess:
    def test_sell_fish_success(self, user_with_fisher_and_fisher_fish):
        """
        GIVEN a user with a fisher profile and a fisher fish
        WHEN the sell_fish_repository is called with valid parameters
        THEN the fisher fish is deleted and the fisher's coins are updated
        """
        user, fisherFish = user_with_fisher_and_fisher_fish
        result = sell_fish_repository(user=user, pk=fisherFish.pk, total_price=1)
        assert result["code"] == "OK"


class TestFishSellRepositoryIntegrationErrors:

    def test_sell_fisher_fish_not_found_error(self, user_with_fisher_and_fisher_fish):
        """
        GIVEN a user with a fisher profile and a fisher fish
        WHEN the sell_fish_repository is called with a non-existent fisher fish pk
        THEN a FisherFishNotFoundError is raised
        """
        user, _ = user_with_fisher_and_fisher_fish
        incorrect__fisher_fish_pk = 999
        with pytest.raises(FisherFishNotFoundError):
            sell_fish_repository(user=user, pk=incorrect__fisher_fish_pk, total_price=1)

    def test_sell_fisher_not_found_error(self, user_without_fisher_profile):
        """
        GIVEN a user without a fisher profile
        WHEN the sell_fish_repository is called with valid parameters
        THEN a FisherNotFoundError is raised
        """
        user = user_without_fisher_profile
        with pytest.raises(FisherNotFoundError):
            sell_fish_repository(user=user, pk=1, total_price=1)
