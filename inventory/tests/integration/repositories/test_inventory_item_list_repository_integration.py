import pytest
from core.exceptions.domain import FisherNotFoundError
from inventory.infrastructure.repositories.inventory_read_repository import (
    get_inventory_item_list_repository,
)
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_item_factory import FisherItemFactory
from inventory.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher_profile_and_fisher_item(db):
    fisher = FisherFactory()
    fisherItem = FisherItemFactory(fisher=fisher)
    return fisher.user, fisherItem


@pytest.fixture
def user_without_fisher_profile(db):
    return UserFactory()


class TestInventoryItemListRepositoryIntegrationSuccess:
    def test_get_inventory_item_list_repository_returns_data(
        self, user_with_fisher_profile_and_fisher_item
    ):
        """
        GIVEN a user with a fisher and purchased items
        WHEN the inventory repository is queried for the user's items
        THEN it returns a list of items with correct code, name and quantity
        """
        user, fisherItem = user_with_fisher_profile_and_fisher_item
        result = get_inventory_item_list_repository(user=user)
        assert result == [
            {
                "item_code": fisherItem.item.code,
                "item_name": fisherItem.item.name,
                "quantity": fisherItem.quantity,
            }
        ]

    def test_get_inventory_item_list_repository_raises_fisher_not_found(
        self, user_without_fisher_profile
    ):
        """
        GIVEN a user without a fisher profile
        WHEN the inventory repository is queried for the user's items
        THEN it raise a FisherNotFoundError
        """
        user = user_without_fisher_profile
        with pytest.raises(FisherNotFoundError) as exc:
            get_inventory_item_list_repository(user=user)
        assert str(exc.value) == FisherNotFoundError.default_detail
