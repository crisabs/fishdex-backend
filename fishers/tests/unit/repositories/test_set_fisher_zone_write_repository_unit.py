from unittest.mock import MagicMock, patch

from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.infrastructure.repositories.fishers_write_repository import (
    set_fisher_zone_repository,
)
import pytest
from fishers.models import Fisher

BASE_PATH = "fishers.infrastructure.repositories.fishers_write_repository."


@pytest.fixture
def fake_user():
    return MagicMock()


class TestSetFisherZoneSuccess:
    @patch(f"{BASE_PATH}transaction")
    @patch(f"{BASE_PATH}Fisher.objects.get")
    def test_set_fisher_zone_returns_success_message(
        self, mock_fisher_get, mock_transaction, fake_user
    ):
        """
        GIVEN a user with an existing fisher profile
        WHEN the repository function is called to update the fisher's zone
        THEN it returns a confirmation message with the new zone
        """
        new_zone = "SEA"
        expected_result = f"Fisher is now in the zone: {new_zone}"
        fake_fisher = MagicMock(coins=1000)
        mock_fisher_get.return_value = fake_fisher
        mock_transaction.return_value.__enter__.return_value = None
        mock_transaction.return_value.__exit__.return_value = None
        result = set_fisher_zone_repository(
            user=fake_user, new_zone=new_zone, zone_cost=100
        )
        assert result == expected_result


class TestSetFisherZoneErrors:
    @patch(f"{BASE_PATH}Fisher.objects.get")
    def test_set_fisher_zone_raises_fisher_not_found_error(
        self, mock_fisher_get, fake_user
    ):
        """
        GIVEN a user with no existing fisher profile
        WHEN the repository function is called to update the fisher's zone
        THEN it raises FisherNotFoundError"""
        new_zone = "SEA"
        mock_fisher_get.side_effect = Fisher.DoesNotExist()
        with pytest.raises(FisherNotFoundError):
            set_fisher_zone_repository(user=fake_user, new_zone=new_zone, zone_cost=100)

    @patch(f"{BASE_PATH}Fisher.objects.get")
    def test_set_fisher_zone_raises_repository_error(self, mock_fisher_get, fake_user):
        """
        GIVEN a user with an existing fisher profile
        WHEN the repository function is called to update the fisher's zone
        THEN it raises RepositoryError if a database error occurs"""
        new_zone = "SEA"
        mock_fisher_get.side_effect = DatabaseError()
        with pytest.raises(RepositoryError):
            set_fisher_zone_repository(user=fake_user, new_zone=new_zone, zone_cost=100)
