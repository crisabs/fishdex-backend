import pytest
from inventory.domain.services.inventory_service import (
    get_inventory_fish_list_repository,
)
from django.utils import timezone

from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory


@pytest.fixture
def user_with_fisher_profile_and_fisher_fish(db):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)
    return fisher.user, fisherFish


@pytest.mark.integration
@pytest.mark.django_db
def test_inventory_fish_list_repository_success_integration(
    user_with_fisher_profile_and_fisher_fish,
):
    """
    GIVEN a user with an associated Fisher profile
    and at least one caught fish in the inventory
    WHEN the repository retrieves the inventory fishes for that user
    THEN it should return a list containing the fish details with correct fields
    """
    user, fisherFish = user_with_fisher_profile_and_fisher_fish

    result = get_inventory_fish_list_repository(user=user)

    assert result[0]["fish__name"] == fisherFish.fish.name
    assert result[0]["pk"] == fisherFish.pk
    assert result[0]["fish__base_price"] == fisherFish.fish.base_price
    assert result[0]["fish__rarity"] == fisherFish.fish.rarity
    assert result[0]["weight"] == fisherFish.weight

    assert isinstance(result[0]["caught_at"], timezone.datetime)
