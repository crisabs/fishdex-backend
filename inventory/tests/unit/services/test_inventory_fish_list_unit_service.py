from decimal import Decimal
import pytest
from unittest.mock import MagicMock, patch
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fish.models import Rarity
from inventory.domain.services.inventory_service import get_inventory_fish_list
from math import floor
from datetime import datetime


@pytest.fixture
def fake_user():
    fake_user = MagicMock(spec=["username"])
    fake_user.username = "user_test@test.com"


class TestInventoryFishListSuccess:
    @patch(
        "inventory.domain.services.inventory_service.get_inventory_fish_list_repository",
        autospec=True,
    )
    def test_inventory_fish_list_unit_service_returns_data(
        self, mock_repository, fake_user
    ):
        caught_at_mock = datetime(2026, 4, 3, 15, 0, 0)
        mock_repository.return_value = [
            {
                "fish__name": "Salmon",
                "fish__base_price": Decimal("1.0"),
                "weight": Decimal("1.0"),
                "pk": 1,
                "caught_at": caught_at_mock,
                "fish__rarity": Rarity.COMMON,
            }
        ]

        result = get_inventory_fish_list(user=fake_user)
        expected_price = floor(
            Decimal(mock_repository.return_value[0]["fish__base_price"])
            * Decimal(mock_repository.return_value[0]["weight"])
        )

        assert result[0]["fish_name"] == mock_repository.return_value[0]["fish__name"]
        assert result[0]["price"] == expected_price
        assert result[0]["weight"] == mock_repository.return_value[0]["weight"]
        assert result[0]["pk"] == mock_repository.return_value[0]["pk"]
        assert result[0]["caught_at"] == mock_repository.return_value[0]["caught_at"]
        assert result[0]["rarity"] == mock_repository.return_value[0]["fish__rarity"]

        mock_repository.assert_called_once_with(user=fake_user)


class TestInventoryFishListErrors:

    @pytest.mark.parametrize("exception_cls", [FisherNotFoundError, RepositoryError])
    @patch(
        "inventory.domain.services.inventory_service.get_inventory_fish_list_repository",
        autospec=True,
    )
    def test_inventory_fish_list_propagate_errors(
        self, mock_repository, fake_user, exception_cls
    ):
        mock_repository.side_effect = exception_cls()
        with pytest.raises(exception_cls) as exc:
            get_inventory_fish_list(user=fake_user)
        assert exc.value.default_detail == exception_cls.default_detail

        mock_repository.assert_called_once()
