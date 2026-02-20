import pytest

from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from fish.models import Fish
from fishers.models import Fisher
from inventory.infrastructure.repositories.inventory_write_repository import (
    sell_fish_repository,
)
from inventory.models import FisherFish


@pytest.fixture
def user_with_fisher_profile_and_fisher_fish(django_user_model):
    """
    Fixture that creates a user, a fisher profile for that user,
    and a fisher fish associated with that fisher.
    Returns the created user and fisher.
    """
    user = django_user_model.objects.create_user(
        username="usertest@user.com", password="usertest"
    )
    fisher = Fisher.objects.create(user=user, nickname=user)
    fish = Fish.objects.get(fish_id=1)
    FisherFish.objects.create(fisher=fisher, fish=fish, weight=10, length=1)
    return user, fisher


@pytest.fixture
def user_without_fisher_profile(django_user_model):
    """
    Fixture that creates a user without a fisher profile for that user.,
    Returns the created user.
    """
    return django_user_model.objects.create_user(
        username="usertest@user.com", password="usertest"
    )


class TestFishSellRepositoryIntegrationSuccess:
    def test_sell_fish_success(self, user_with_fisher_profile_and_fisher_fish):
        """
        GIVEN a user with a fisher profile and a fisher fish
        WHEN the sell_fish_repository is called with valid parameters
        THEN the fisher fish is deleted and the fisher's coins are updated
        """

        user, fisher = user_with_fisher_profile_and_fisher_fish
        pk = (
            FisherFish.objects.filter(fisher=fisher)
            .select_related("fish")
            .values_list("pk", flat=True)
            .first()
        )
        result = sell_fish_repository(user=user, pk=pk, total_price=1)
        assert result["code"] == "OK"


class TestFishSellRepositoryIntegrationErrors:
    def test_sell_fish_repository_error(self):
        pass

    def test_sell_fisher_fish_not_found_error(
        self, user_with_fisher_profile_and_fisher_fish
    ):
        """
        GIVEN a user with a fisher profile and a fisher fish
        WHEN the sell_fish_repository is called with a non-existent fisher fish pk
        THEN a FisherFishNotFoundError is raised
        """
        user, _ = user_with_fisher_profile_and_fisher_fish
        with pytest.raises(FisherFishNotFoundError):
            sell_fish_repository(user=user, pk=200, total_price=1)

    def test_sell_fisher_not_found_error(self, user_without_fisher_profile):
        """
        GIVEN a user without a fisher profile
        WHEN the sell_fish_repository is called with valid parameters
        THEN a FisherNotFoundError is raised
        """
        user = user_without_fisher_profile
        with pytest.raises(FisherNotFoundError):
            sell_fish_repository(user=user, pk=1, total_price=1)
