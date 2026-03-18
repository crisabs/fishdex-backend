from unittest.mock import MagicMock, patch

from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.infrastructure.repositories.fishers_write_repository import (
    set_fisher_nickname_repository,
)
from fishers.models import Fisher
import pytest


@pytest.fixture
def fake_user():
    return MagicMock()


class TestFisherNicknameSuccess:
    @patch("fishers.infrastructure.repositories.fishers_write_repository.transaction")
    @patch(
        "fishers.infrastructure.repositories.fishers_write_repository.Fisher.objects.get"
    )
    def test_fisher_nickname_returns_confirmation_message(
        self, mock_fisher_get, mock_transaction, fake_user
    ):
        """
        GIVEN a user with an existing fisher profile
        WHEN the repository function is called to update the fisher's nickname
        THEN it returns a confirmation message with the new nickname
        """
        new_nickname = "new_nickname"
        expected_result = f"Fisher nickname updated to {new_nickname}"

        fake_fisher = MagicMock()
        mock_fisher_get.return_value = fake_fisher

        mock_transaction.return_value.__enter__.return_value = None
        mock_transaction.return_value.__exit__.return_value = None

        result = set_fisher_nickname_repository(user=fake_user, nickname=new_nickname)
        assert result == expected_result


class TestFisherNicknameErrors:

    @patch("fishers.infrastructure.repositories.fishers_write_repository.transaction")
    @patch(
        "fishers.infrastructure.repositories.fishers_write_repository.Fisher.objects.get"
    )
    def test_fisher_nickname_raises_fisher_not_found_error(
        self, mock_fisher_get, mock_transaction, fake_user
    ):
        """
        GIVEN a user with no existing fisher profile
        WHEN the repository function is called to update the fisher's nickname
        THEN it raises FisherNotFoundError
        """
        mock_fisher_get.side_effect = Fisher.DoesNotExist()
        mock_transaction.return_value.__enter__.return_value = None
        mock_transaction.return_value.__exit__.return_value = None

        with pytest.raises(FisherNotFoundError):
            set_fisher_nickname_repository(user=fake_user, nickname="new_nickname")

    @patch("fishers.infrastructure.repositories.fishers_write_repository.transaction")
    @patch(
        "fishers.infrastructure.repositories.fishers_write_repository.Fisher.objects.get"
    )
    def test_fisher_nickname_raises_repository_error(
        self, mock_fisher_get, mock_transaction, fake_user
    ):
        """
        GIVEN a user with an existing fisher profile
        WHEN the repository function is called to update the fisher's nickname
        THEN it raises RepositoryError if a database error occurs
        """
        mock_fisher_get.side_effect = DatabaseError()
        mock_transaction.return_value.__enter__.return_value = None
        mock_transaction.return_value.__exit__.return_value = None

        with pytest.raises(RepositoryError):
            set_fisher_nickname_repository(user=fake_user, nickname="new_nickname")
