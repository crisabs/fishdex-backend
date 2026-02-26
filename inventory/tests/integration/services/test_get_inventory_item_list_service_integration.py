import pytest
from core.exceptions.domain import FisherNotFoundError
from inventory.domain.services.inventory_service import get_inventory_item_list
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_item_factory import FisherItemFactory
from inventory.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher_profile_and_items(db):
    fisher = FisherFactory()
    fisher_item = FisherItemFactory(fisher=fisher)
    return fisher.user, fisher_item


@pytest.fixture
def user_without_fisher_profile(db):
    return UserFactory()


class TestGetInventoryItemListServiceSuccess:

    def test_get_inventory_item_list_service_returns_data(
        self, user_with_fisher_profile_and_items
    ):
        """
        GIVEN a valid user and the repository returns a list of inventory items
        WHEN the inventory service is called
        THEN the service returns the item list as provided by the repository
        """
        user, fisherItem = user_with_fisher_profile_and_items
        expected_value = [
            {
                "item_code": fisherItem.item.code,
                "item_name": fisherItem.item.name,
                "quantity": fisherItem.quantity,
            },
        ]
        result = get_inventory_item_list(user=user)
        assert result == expected_value
        assert result[0]["item_code"] == expected_value[0]["item_code"]


class TestGetInventoryItemListServiceErrors:

    def test_get_inventory_item_list_service_raises_fisher_not_found(
        self, user_without_fisher_profile
    ):
        """
        GIVEN a valid user and the repository raises a FisherNotFoundError
        WHEN the inventory service is called
        THEN the service propagates the FisherNotFoundError
        """

        with pytest.raises(FisherNotFoundError):
            get_inventory_item_list(user=user_without_fisher_profile)
