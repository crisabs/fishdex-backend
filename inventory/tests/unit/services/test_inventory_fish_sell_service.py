import pytest
from decimal import Decimal
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from inventory.domain.services.inventory_service import sell_fish
from unittest.mock import patch


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )


@pytest.fixture
def sell_fish_params():
    """Fixture providing standard parameters for sell_fish method."""
    return {
        "pk": 1,
        "fish_id": 42,
        "total_weight": 2.5,
    }


class TestSellFishSuccess:
    """Test cases for successful sell_fish operations."""

    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    def test_sell_fish_success_returns_ok_response(
        self, mock_get_price, mock_repository, user, sell_fish_params
    ):
        """
        GIVEN a valid user, valid inventory primary key, valid fish ID, and valid weight
        WHEN the sell_fish service is called
        THEN the service returns a successful response with code 'OK'
        """

        mock_get_price.return_value = Decimal("250.00")
        mock_repository.return_value = {"code": "OK"}

        result = sell_fish(
            user=user,
            pk=sell_fish_params["pk"],
            fish_id=sell_fish_params["fish_id"],
            total_weight=sell_fish_params["total_weight"],
        )

        assert result == {"code": "OK"}

    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    def test_sell_fish_success_calls_get_price_correctly(
        self, mock_get_price, mock_repository, user, sell_fish_params
    ):
        """
        GIVEN valid parameters for selling a fish
        WHEN the sell_fish service is called
        THEN the get_price_fish_to_sell is called with
        the correct fish_id and total_weight
        """

        mock_get_price.return_value = Decimal("100.00")
        mock_repository.return_value = {"code": "OK"}

        sell_fish(
            user=user,
            pk=sell_fish_params["pk"],
            fish_id=sell_fish_params["fish_id"],
            total_weight=sell_fish_params["total_weight"],
        )

        mock_get_price.assert_called_once_with(
            fish_id=sell_fish_params["fish_id"],
            total_weight=sell_fish_params["total_weight"],
        )

    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    def test_sell_fish_success_calls_repository_with_correct_params(
        self, mock_get_price, mock_repository, user, sell_fish_params
    ):
        """
        GIVEN a calculated total price from get_price_fish_to_sell
        WHEN the sell_fish service is called
        THEN the sell_fish_repository is called with user, pk,
        and the calculated total_price
        """

        expected_price = Decimal("350.50")
        mock_get_price.return_value = expected_price
        mock_repository.return_value = {"code": "OK"}

        sell_fish(
            user=user,
            pk=sell_fish_params["pk"],
            fish_id=sell_fish_params["fish_id"],
            total_weight=sell_fish_params["total_weight"],
        )

        mock_repository.assert_called_once_with(
            user=user,
            pk=sell_fish_params["pk"],
            total_price=expected_price,
        )

    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    def test_sell_fish_success_with_different_weights(
        self, mock_get_price, mock_repository, user
    ):
        """
        GIVEN different total_weight values
        WHEN the sell_fish service is called multiple times
        THEN each call calculates the correct price for the respective weight
        """

        weights = [1.0, 5.5, 10.0]
        prices = [Decimal("100"), Decimal("550"), Decimal("1000")]

        mock_repository.return_value = {"code": "OK"}

        for weight, price in zip(weights, prices):
            mock_get_price.return_value = price

            result = sell_fish(
                user=user,
                pk=1,
                fish_id=42,
                total_weight=weight,
            )

            assert result == {"code": "OK"}


class TestSellFishErrors:
    """Test cases for sell_fish error handling."""

    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    def test_sell_fish_raises_fisher_not_found_error(
        self, mock_get_price, mock_repository, user, sell_fish_params
    ):
        """
        GIVEN a valid user but the repository cannot find the associated fisher
        WHEN the sell_fish service is called
        THEN the service propagates the FisherNotFoundError from the repository
        """

        mock_get_price.return_value = Decimal("250.00")
        mock_repository.side_effect = FisherNotFoundError()

        with pytest.raises(FisherNotFoundError):
            sell_fish(
                user=user,
                pk=sell_fish_params["pk"],
                fish_id=sell_fish_params["fish_id"],
                total_weight=sell_fish_params["total_weight"],
            )

    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    def test_sell_fish_raises_repository_error(
        self, mock_get_price, mock_repository, user, sell_fish_params
    ):
        """
        GIVEN valid parameters but the repository encounters a database error
        WHEN the sell_fish service is called
        THEN the service propagates the RepositoryError from the repository
        """

        mock_get_price.return_value = Decimal("250.00")
        mock_repository.side_effect = RepositoryError()

        with pytest.raises(RepositoryError):
            sell_fish(
                user=user,
                pk=sell_fish_params["pk"],
                fish_id=sell_fish_params["fish_id"],
                total_weight=sell_fish_params["total_weight"],
            )

    @patch("inventory.domain.services.inventory_service.sell_fish_repository")
    @patch("inventory.domain.services.inventory_service.get_price_fish_to_sell")
    def test_sell_fish_error_prevents_repository_call_after_price_calculation_failure(
        self, mock_get_price, mock_repository, user, sell_fish_params
    ):
        """
        GIVEN a failure in the price calculation
        WHEN the sell_fish service is called
        THEN the repository is not called and the exception is propagated
        """

        from core.exceptions.domain import FishNotFoundError

        mock_get_price.side_effect = FishNotFoundError()

        with pytest.raises(FishNotFoundError):
            sell_fish(
                user=user,
                pk=sell_fish_params["pk"],
                fish_id=sell_fish_params["fish_id"],
                total_weight=sell_fish_params["total_weight"],
            )

        mock_repository.assert_not_called()
