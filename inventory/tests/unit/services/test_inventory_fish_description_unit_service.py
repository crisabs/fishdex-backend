from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from inventory.domain.services.inventory_service import set_description_fisher_fish
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def valid_request_data():
    return {"pk": 1, "description": "This fish was hard to find"}


@pytest.fixture
def fake_user():
    fake_user = MagicMock(spec=["username", "password"])
    fake_user.username = "user_test@test.com"
    fake_user.password = "hashed-password"
    return fake_user


class TestInventoryFishDescriptionSuccess:
    @patch(
        "inventory.domain.services.inventory_service.set_description_fisher_fish_repository",
        autospec=True,
    )
    def test_inventory_fish_description_unit_api_returns_data(
        self, mock_repository, valid_request_data, fake_user
    ):
        mock_repository.return_value = {"code": "OK"}

        result = set_description_fisher_fish(
            user=fake_user,
            pk=valid_request_data["pk"],
            description=valid_request_data["description"],
        )

        assert result == mock_repository.return_value

        mock_repository.assert_called_once_with(
            user=fake_user,
            pk=valid_request_data["pk"],
            description=valid_request_data["description"],
        )


class TestInventoryFishDescriptionErrors:
    @pytest.mark.parametrize(
        "exception_cls", [FisherNotFoundError, FisherFishNotFoundError, RepositoryError]
    )
    @patch(
        "inventory.domain.services.inventory_service.set_description_fisher_fish_repository",
        autospec=True,
    )
    def test_inventory_fish_description_propagates_errors(
        self, mock_repository, valid_request_data, fake_user, exception_cls
    ):
        mock_repository.side_effect = exception_cls()
        with pytest.raises(exception_cls) as exc:
            set_description_fisher_fish(
                user=fake_user,
                pk=valid_request_data["pk"],
                description=valid_request_data["description"],
            )
        assert exc.value.default_detail == exception_cls.default_detail
        mock_repository.assert_called_once()
