import pytest
from fishers.models import Fisher
from inventory.infrastructure.repositories.inventory_read_repository import (
    get_inventory_item_list_repository,
)
from inventory.models import FisherItem
from store.models import ItemStore


@pytest.fixture
def user_with_items(django_user_model):
    """
    GIVEN a user with fisher and pre-purchased items
    """
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )
    fisher = Fisher.objects.create(user=user, nickname="user_test")
    itemStore, _ = ItemStore.objects.get_or_create(
        code="ROD_BASIC", defaults={"name": "Basic Rod", "price": 100, "effect": 0.2}
    )

    FisherItem.objects.update_or_create(
        fisher=fisher, item=itemStore, defaults={"quantity": 1}
    )
    return user


@pytest.mark.integration
@pytest.mark.django_db
def test_get_inventory_item_list_repository_returns_data(user_with_items):
    """
    GIVEN a user with a fisher and purchased items
    WHEN the inventory repository is queried for the user's items
    THEN it returns a list of items with correct code, name and quantity
    """
    result = get_inventory_item_list_repository(user=user_with_items)
    assert result == [
        {"item_code": "ROD_BASIC", "item_name": "Basic Rod", "quantity": 1}
    ]
