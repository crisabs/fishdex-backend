import pytest
from unittest.mock import patch, MagicMock
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from inventory.domain.services.inventory_service import get_inventory_item_list


@pytest.fixture
def fake_user():
    fake_user = MagicMock(specs=["username"])
    fake_user.username = "usertest@test.com"
    return fake_user


class TestInventoryItemListSuccess:
    @patch(
        "inventory.domain.services.inventory_service.get_inventory_item_list_repository"
    )
    def test_inventory_item_list_returns_data(self, mock_repository, fake_user):
        """
        GIVEN a valid user
        WHEN the get_inventory_item_list service is called
        THEN it should return the expected result and call the repository with correct parameters
        """
        mock_repository.return_value = [
            {"item_code": 1, "item_name": "Basic Rod", "quantity": 1},
        ]
        result = get_inventory_item_list(user=fake_user)
        assert result == mock_repository.return_value

        mock_repository.assert_called_once_with(user=fake_user)


class TestInventoryItemListErrors:
    @pytest.mark.parametrize("exception_cls", [FisherNotFoundError, RepositoryError])
    @patch(
        "inventory.domain.services.inventory_service.get_inventory_item_list_repository"
    )
    def test_inventory_item_list_propagates_errors(
        self, mock_repository, fake_user, exception_cls
    ):
        """
        GIVEN a valid user
        WHEN the get_inventory_item_list service is called and the repository raises an exception
        THEN it should propagate the exception and log the error
        """
        mock_repository.side_effect = exception_cls()
        with pytest.raises(exception_cls):
            get_inventory_item_list(user=fake_user)

        mock_repository.assert_called_once_with(user=fake_user)
