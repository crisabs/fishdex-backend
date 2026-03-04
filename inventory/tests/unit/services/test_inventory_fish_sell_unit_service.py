from unittest.mock import MagicMock, patch
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import (
    FisherFishNotFoundError,
    FisherNotFoundError,
)
from inventory.domain.services.inventory_service import sell_fish
import pytest


@pytest.fixture
def sell_data_params():
    user = MagicMock(specs=["username"])
    user.username = "usertest@user.com"
    return {"user": user, "fish_id": 1, "total_weight": 1.0, "pk": 1}


class TestInventoryFishSellSuccess:
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    def test_inventory_fish_sell_returns_data(
        self, mock_sell_fish_repository, mock_price, sell_data_params
    ):
        """
        GIVEN a valid user, fish_id, total_weight and pk
        WHEN the sell_fish service is called
        THEN it should return the expected result and call the repository with correct parameters
        """
        mock_sell_fish_repository.return_value = {"code": "OK"}
        mock_price.return_value = 100

        result = sell_fish(
            user=sell_data_params["user"],
            pk=sell_data_params["pk"],
            fish_id=sell_data_params["fish_id"],
            total_weight=sell_data_params["total_weight"],
        )

        assert result == mock_sell_fish_repository.return_value

        mock_price.assert_called_once_with(
            fish_id=sell_data_params["fish_id"],
            total_weight=sell_data_params["total_weight"],
        )

        mock_sell_fish_repository.assert_called_once_with(
            user=sell_data_params["user"],
            pk=sell_data_params["pk"],
            total_price=mock_price.return_value,
        )


class TestInventoryFishSellErrors:
    @pytest.mark.parametrize(
        "exception_cls",
        [
            FisherNotFoundError,
            FisherFishNotFoundError,
            RepositoryError,
        ],
    )
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    def test_inventory_fish_sell_propagate_errors(
        self, mock_sell_fish_repository, mock_price, sell_data_params, exception_cls
    ):
        """
        GIVEN a valid user, fish_id, total_weight and pk
        WHEN the sell_fish service is called and the repository raises an exception
        THEN it should propagate the exception and log the error
        """
        mock_price.return_value = 100
        mock_sell_fish_repository.side_effect = exception_cls()
        with pytest.raises(exception_cls):
            sell_fish(
                user=sell_data_params["user"],
                pk=sell_data_params["pk"],
                fish_id=sell_data_params["fish_id"],
                total_weight=sell_data_params["total_weight"],
            )

        mock_price.assert_called_once_with(
            fish_id=sell_data_params["fish_id"],
            total_weight=sell_data_params["total_weight"],
        )
        mock_sell_fish_repository.assert_called_once()
