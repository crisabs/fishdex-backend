import pytest
from decimal import Decimal
from core.exceptions.domain import (
    FisherNotFoundError,
    FishNotFoundError,
)
from inventory.domain.services.inventory_service import sell_fish
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory
from inventory.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher_profile_and_fisher_fish(db):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)
    return fisher.user, fisherFish


@pytest.fixture
def user_without_fisher_profile(db):
    return UserFactory()


class TestSellFishSuccess:
    """Test cases for successful sell_fish operations."""

    def test_sell_fish_success_returns_ok_response(
        self,
        user_with_fisher_profile_and_fisher_fish,
    ):
        """
        GIVEN a valid user, valid inventory primary key, valid fish ID, and valid weight
        WHEN the sell_fish service is called
        THEN the service returns a successful response with code 'OK'
        """
        user, fisherFish = user_with_fisher_profile_and_fisher_fish
        expected_return_value = {"code": "OK"}

        result = sell_fish(
            user=user,
            pk=fisherFish.pk,
            fish_id=fisherFish.fish.fish_id,
            total_weight=Decimal("2.5"),
        )

        assert result == expected_return_value


class TestSellFishErrors:
    """Test cases for sell_fish error handling."""

    def test_sell_fish_raises_fisher_not_found(self, user_without_fisher_profile):
        """
        GIVEN a valid user but the repository cannot find the associated fisher
        WHEN the sell_fish service is called
        THEN the service propagates the FisherNotFoundError from the repository
        """
        with pytest.raises(FisherNotFoundError) as exc:
            sell_fish(
                user=user_without_fisher_profile,
                pk=1,
                fish_id=1,
                total_weight=Decimal(2.5),
            )
        assert str(exc.value) == FisherNotFoundError.default_detail

    def test_sell_fish_raises_fisher_fish_not_found(
        self, user_with_fisher_profile_and_fisher_fish
    ):
        """
        GIVEN a valid user but the repository cannot find the associated fisher fish
        WHEN the sell_fish service is called
        THEN the service propagates the FisherFishNotFoundError from the repository
        """
        with pytest.raises(FishNotFoundError) as exc:
            sell_fish(
                user=user_with_fisher_profile_and_fisher_fish,
                pk=1,
                fish_id=-11,
                total_weight=Decimal(2.5),
            )
        assert str(exc.value) == FishNotFoundError.default_detail
