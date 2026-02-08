import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from inventory.domain.services.inventory_service import get_inventory_item_list
from unittest.mock import patch


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )


@patch("inventory.domain.services.inventory_service.get_inventory_item_list_repository")
def test_get_inventory_item_list_service_returns_data(mock_repository, user):
    """
    GIVEN a valid user and the repository returns a list of inventory items
    WHEN the inventory service is called
    THEN the service returns the item list as provided by the repository
    """

    mock_repository.return_value = [
        {"item_code": "ROD_BASIC", "item_name": "Basic Rod", "quantity": 1},
    ]
    result = get_inventory_item_list(user=user)
    assert result == mock_repository.return_value


@patch("inventory.domain.services.inventory_service.get_inventory_item_list_repository")
def test_get_inventory_item_list_service_raises_fisher_not_found_error(
    mock_repository, user
):
    """
    GIVEN a valid user and the repository raises a FisherNotFoundError
    WHEN the inventory service is called
    THEN the service propagates the FisherNotFoundError
    """

    mock_repository.side_effect = FisherNotFoundError()
    with pytest.raises(FisherNotFoundError):
        get_inventory_item_list(user=user)


@patch("inventory.domain.services.inventory_service.get_inventory_item_list_repository")
def test_get_inventory_item_list_service_raises_repository_error(mock_repository, user):
    """
    GIVEN a valid user and the repository raises a RepositoryError
    WHEN the inventory service is called
    THEN the service propagates the RepositoryError
    """

    mock_repository.side_effect = RepositoryError()
    with pytest.raises(RepositoryError):
        get_inventory_item_list(user=user)
