from core.exceptions.domain import FisherNotFoundError
from inventory.domain.services.inventory_service import get_inventory_fish_list
import pytest
from decimal import Decimal
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory
from inventory.tests.factories.user_factory import UserFactory
from math import floor


@pytest.fixture
def user_with_fisher_profile_and_fish(db):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)
    return fisher.user, fisherFish


@pytest.fixture
def user_without_fisher_profile(db):
    return UserFactory()


class TestGetInventoryFishListServiceSuccess:

    def test_get_inventory_fish_list_service_returns_data(
        self, user_with_fisher_profile_and_fish
    ):
        """
        GIVEN a user with a fisher profile
        WHEN get_inventory_fish_list is called
        THEN it should return the expected list of fishes with correct data
        """
        user, fisherFish = user_with_fisher_profile_and_fish
        price = floor(Decimal(fisherFish.fish.base_price * Decimal(fisherFish.weight)))
        expected_result = [
            {
                "fish_name": fisherFish.fish.name,
                "price": price,
                "pk": fisherFish.pk,
                "weight": fisherFish.weight,
                "caught_at": fisherFish.caught_at,
                "rarity": fisherFish.fish.rarity,
            }
        ]
        result = get_inventory_fish_list(user=user)
        assert result == expected_result
        assert result[0]["pk"] == fisherFish.pk
        assert result[0]["price"] == price


class TestGetInventoryFishListServiceErrors:

    def test_get_inventory_fish_list_service_raises_fisher_not_found_error(
        self, user_without_fisher_profile
    ):
        """
        GIVEN a user without a fisher profile
        WHEN get_inventory_fish_list is called
        THEN it should raise FisherNotFoundError
        """

        with pytest.raises(FisherNotFoundError) as exc:
            get_inventory_fish_list(user=user_without_fisher_profile)

        assert str(exc.value) == FisherNotFoundError.default_detail
