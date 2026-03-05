import datetime
from decimal import Decimal

import pytest
from unittest.mock import MagicMock, patch
from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher
from fish.models import Rarity
from inventory.infrastructure.repositories.inventory_read_repository import (
    get_inventory_fish_list_repository,
)


@pytest.fixture
def fake_user():
    fake_user = MagicMock(specs=["username"])
    fake_user.username = "usertest@test.com"
    return fake_user


class TestInventoryFishListSuccess:
    @patch(
        "inventory.infrastructure.repositories.inventory_read_repository.FisherFish.objects.filter",
        autospec=True,
    )
    @patch(
        "inventory.infrastructure.repositories.inventory_read_repository.Fisher.objects.get",
        autospec=True,
    )
    def test_inventory_fish_list_returns_list(
        self, mock_fisher_get, mock_fisher_fish_filter, fake_user
    ):
        """
        GIVEN a user with an associated Fisher profile and caught fishes
        WHEN get_inventory_fish_list_repository is called
        THEN it should return a list of inventory fishes with their details.
        """
        caught_at_expected = datetime.datetime(2026, 1, 1, 1, 0)
        expected_result = [
            {
                "fish__name": "Salmon",
                "fish__base_price": Decimal("1.0"),
                "weight": Decimal("1.0"),
                "pk": 1,
                "caught_at": caught_at_expected,
                "fish__rarity": Rarity.COMMON,
            }
        ]
        fake_fisher = MagicMock()
        mock_fisher_get.return_value = fake_fisher

        queryset_mock = MagicMock()
        queryset_mock.select_related.return_value.values.return_value = expected_result

        mock_fisher_fish_filter.return_value = queryset_mock

        result = get_inventory_fish_list_repository(user=fake_user)
        assert result == expected_result

        mock_fisher_get.assert_called_once_with(user=fake_user)
        mock_fisher_fish_filter.assert_called_once_with(fisher=fake_fisher)
        queryset_mock.select_related.assert_called_once_with("fish")
        queryset_mock.select_related.return_value.values.assert_called_once_with(
            "fish__name",
            "fish__base_price",
            "weight",
            "pk",
            "caught_at",
            "fish__rarity",
        )


class TestInventoryFishListErrors:
    @patch(
        "inventory.infrastructure.repositories.inventory_read_repository.Fisher.objects.get",
        autospec=True,
    )
    def test_inventory_fish_list_raises_fisher_do_not_exist(
        self, mock_fisher_get, fake_user
    ):
        """
        GIVEN a user without an associated Fisher profile
        WHEN get_inventory_fish_list_repository is called
        THEN it should raise a FisherNotFoundError."""

        mock_fisher_get.side_effect = Fisher.DoesNotExist()
        with pytest.raises(FisherNotFoundError):
            get_inventory_fish_list_repository(user=fake_user)

        mock_fisher_get.assert_called_once_with(user=fake_user)

    @patch(
        "inventory.infrastructure.repositories.inventory_read_repository.Fisher.objects.get",
        autospec=True,
    )
    def test_inventory_fish_list_raises_repository_error(
        self, mock_fisher_get, fake_user
    ):
        """
        GIVEN a database error occurs when retrieving the Fisher profile
        WHEN get_inventory_fish_list_repository is called
        THEN it should raise a RepositoryError."""
        mock_fisher_get.side_effect = DatabaseError()
        with pytest.raises(RepositoryError):
            get_inventory_fish_list_repository(user=fake_user)
        mock_fisher_get.assert_called_once_with(user=fake_user)

    @patch(
        "inventory.infrastructure.repositories.inventory_read_repository.FisherFish.objects.filter"
    )
    @patch(
        "inventory.infrastructure.repositories.inventory_read_repository.Fisher.objects.get"
    )
    def test_inventory_fish_list_fisher_invalid_result(
        self, mock_fisher, mock_fisher_fish_filter, fake_user
    ):
        """
        GIVEN a user with an associated Fisher profile and caught fishes
        WHEN get_inventory_fish_list_repository is called but the query returns an invalid result
        THEN it should not match the expected result and
        should raise an error when trying to access missing fields.
        """

        expected_result = [
            {
                "fish__name": "Salmon",
                "fish__base_price": Decimal("1.0"),
                "weight": Decimal("1.0"),
                "pk": 1,
                "caught_at": datetime.datetime(2006, 1, 1, 1, 1),
                "fish__rarity": Rarity.COMMON,
            },
        ]

        invalid_result = [
            {
                "fish__name": "Salmon",
                "fish__base_price": Decimal("1.0"),
                "pk": 1,
                "caught_at": datetime.datetime(2006, 1, 1, 1, 1),
                "fish__rarity": Rarity.COMMON,
            },
        ]

        fake_fisher = MagicMock()
        mock_fisher.return_value = fake_fisher

        query_mock = MagicMock()
        query_mock.select_related.return_value.values.return_value = invalid_result

        mock_fisher_fish_filter.return_value = query_mock

        result = get_inventory_fish_list_repository(user=fake_user)

        assert result != expected_result

        mock_fisher.assert_called_once_with(user=fake_user)
        mock_fisher_fish_filter.assert_called_once_with(fisher=fake_fisher)
        query_mock.select_related.assert_called_once_with("fish")
        query_mock.select_related.return_value.values.assert_called_once_with(
            "fish__name",
            "fish__base_price",
            "weight",
            "pk",
            "caught_at",
            "fish__rarity",
        )
