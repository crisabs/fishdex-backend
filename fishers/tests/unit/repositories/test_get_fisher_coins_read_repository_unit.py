from unittest.mock import MagicMock, patch

from django.db import DatabaseError
import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.infrastructure.repositories.fishers_read_repository import get_fisher_coins
from fishers.models import Fisher

COINS_VALID = 250


@pytest.fixture
def user():
    fake_user = MagicMock()
    return fake_user


class TestFisherCoinsSuccess:
    @patch(
        "fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get"
    )
    def test_fisher_coins_returns_coins(self, mock_fisher, user):
        """
        GIVEN a user with an existing fisher profile
        WHEN the repository function is called to fetch the user's coin balance
        THEN it returns the number of coins if the fisher exists
        """

        fake_fisher = MagicMock(coins=COINS_VALID)
        mock_fisher.return_value = fake_fisher

        result = get_fisher_coins(user=user)
        assert result == COINS_VALID


class TestFisherCoinsErrors:
    @patch(
        "fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get"
    )
    def test_fisher_coins_returns_raises_fisher_not_found_error(
        self, mock_fisher_get, user
    ):
        """
        GIVEN a user with no existing fisher profile
        WHEN the repository function is called to fetch the user's coin balance
        THEN it raises FisherNotFoundError"""
        mock_fisher_get.side_effect = Fisher.DoesNotExist
        with pytest.raises(FisherNotFoundError):
            get_fisher_coins(user=user)

    @patch(
        "fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get"
    )
    def test_fisher_coins_returns_raises_repository_error(self, mock_fisher_get, user):
        """
        GIVEN a user with no existing fisher profile
        WHEN the repository function is called to fetch the user's coin balance
        THEN it raises RepositoryError"""
        mock_fisher_get.side_effect = DatabaseError
        with pytest.raises(RepositoryError):
            get_fisher_coins(user=user)
