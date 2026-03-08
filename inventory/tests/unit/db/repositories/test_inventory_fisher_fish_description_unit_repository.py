from typing import Tuple

from django.db import DatabaseError
import pytest
from unittest.mock import MagicMock, patch
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from inventory.infrastructure.repositories.inventory_write_repository import (
    set_description_fisher_fish_repository,
)
from fishers.models import Fisher
from inventory.models import FisherFish
from django.contrib.auth.models import AbstractBaseUser

MODULE_PATH = "inventory.infrastructure.repositories.inventory_write_repository"


@pytest.fixture
def fake_user():
    fake_user = MagicMock(specs=["username"])
    fake_user.username = "usertest@test.com"
    return fake_user


@pytest.fixture
def valid_description_params(fake_user) -> Tuple[AbstractBaseUser, int, str]:
    return fake_user, 1, "x" * 25


class TestFisherFishDescriptionSuccess:
    @patch(f"{MODULE_PATH}.transaction.atomic", autospec=True)
    @patch(f"{MODULE_PATH}.FisherFish.objects.get", autospec=True)
    @patch(f"{MODULE_PATH}.Fisher.objects.get", autospec=True)
    def test_description_fisher_fish_returns_data(
        self,
        mock_fisher_get,
        mock_fisher_fish_get,
        mock_transaction,
        valid_description_params,
    ):
        """
        GIVEN a valid user, pk and description
        WHEN set_description_fisher_fish_repository is called
        THEN it should return a success response and update the description of the fisher fish
        """
        fake_fisher = MagicMock()
        mock_fisher_get.return_value = fake_fisher

        fake_fisher_fish = MagicMock()
        mock_fisher_fish_get.return_value = fake_fisher_fish

        expected_result = {"success": True}

        mock_transaction.return_value.__enter__.return_value = None
        mock_transaction.return_value.__exit__.return_value = None

        user, pk, description = valid_description_params

        result = set_description_fisher_fish_repository(
            user=user,
            pk=pk,
            description=description,
        )
        assert result == expected_result

        mock_fisher_get.assert_called_once_with(user=user)
        mock_fisher_fish_get.assert_called_once_with(fisher=fake_fisher, pk=pk)
        mock_transaction.assert_called_once()


class TestFisherFishDescriptionErrors:
    @patch(
        f"{MODULE_PATH}.Fisher.objects.get",
        autospec=True,
    )
    def test_description_fisher_not_found(
        self, mock_fisher_get, valid_description_params
    ):
        """
        GIVEN a user that does not have an associated fisher profile
        WHEN set_description_fisher_fish_repository is called
        THEN it should raise a FisherNotFoundError"""
        mock_fisher_get.side_effect = Fisher.DoesNotExist()
        user, pk, description = valid_description_params
        with pytest.raises(FisherNotFoundError):
            set_description_fisher_fish_repository(
                user=user,
                pk=pk,
                description=description,
            )
        mock_fisher_get.assert_called_once_with(user=user)

    @patch(
        f"{MODULE_PATH}.FisherFish.objects.get",
        autospec=True,
    )
    @patch(
        f"{MODULE_PATH}.Fisher.objects.get",
        autospec=True,
    )
    def test_description_fisher_fish_not_found(
        self, mock_fisher_get, mock_fisher_fish_get, valid_description_params
    ):

        fake_fisher = MagicMock()
        mock_fisher_get.return_value = fake_fisher

        mock_fisher_fish_get.side_effect = FisherFish.DoesNotExist()

        user, pk, description = valid_description_params

        with pytest.raises(FisherFishNotFoundError):
            set_description_fisher_fish_repository(
                user=user,
                pk=pk,
                description=description,
            )
        mock_fisher_get.assert_called_once_with(user=user)
        mock_fisher_fish_get.assert_called_once_with(fisher=fake_fisher, pk=pk)

    @patch(f"{MODULE_PATH}.transaction.atomic", autospec=True)
    @patch(f"{MODULE_PATH}.FisherFish.objects.get", autospec=True)
    @patch(f"{MODULE_PATH}.Fisher.objects.get", autospec=True)
    def test_description_invalid_data_raises_database_error(
        self,
        mock_fisher_get,
        mock_fisher_fish_get,
        mock_transaction_atomic,
        valid_description_params,
    ):
        """
        GIVEN a valid user, pk and an invalid description that exceeds the maximum length
        WHEN set_description_fisher_fish_repository is called
        THEN it should raise a RepositoryError due to a DatabaseError
        when trying to save the invalid description
        """
        fake_fisher = MagicMock()
        mock_fisher_get.return_value = fake_fisher

        fisher_fish = MagicMock()
        mock_fisher_fish_get.return_value = fisher_fish

        mock_transaction_atomic.return_value.__enter__.return_value = None
        mock_transaction_atomic.return_value.__exit__.return_value = None

        fisher_fish.save.side_effect = DatabaseError()

        user, pk, _ = valid_description_params
        invalid_description = "x" * 300

        with pytest.raises(RepositoryError):
            set_description_fisher_fish_repository(
                user=user, pk=pk, description=invalid_description
            )
