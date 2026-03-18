from unittest.mock import MagicMock, patch

from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.infrastructure.repositories.fishers_read_repository import (
    get_fisher_details_me_repository,
)
from fishers.models import Fisher
import pytest


@pytest.fixture
def fake_user():
    fake_user = MagicMock()
    return fake_user


class TestFisherDetailsMeSuccess:
    @patch(
        "fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get"
    )
    def test_fisher_details_me_returns_data(self, mock_fisher_get, fake_user):
        """
        GIVEN a user with an existing fisher profile
        WHEN the repository function is called to fetch the fisher's details
        THEN it returns the fisher's nickname, level,
        counts, and current zone if the record
        """
        fake_fisher = MagicMock()
        fake_fisher.nickname = "fake_nickname"
        fake_fisher.level = 10
        fake_fisher.coins = 120
        fake_fisher.current_zone = "LAKE"

        mock_fisher_get.return_value = fake_fisher
        result = get_fisher_details_me_repository(user=fake_user)

        assert result["nickname"] == fake_fisher.nickname
        assert result["level"] == fake_fisher.level
        assert result["coins"] == fake_fisher.coins
        assert result["current_zone"] == fake_fisher.current_zone


class TestFisherDetailsMeErrors:
    @patch(
        "fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get"
    )
    def test_fisher_details_me_raises_fisher_not_found_error(
        self, mock_fisher_get, fake_user
    ):
        """
        GIVEN a user with no existing fisher profile
        WHEN the repository function is called to fetch the fisher's details
        THEN it raises FisherNotFoundError"""
        mock_fisher_get.side_effect = Fisher.DoesNotExist
        with pytest.raises(FisherNotFoundError):
            get_fisher_details_me_repository(user=fake_user)

    @patch(
        "fishers.infrastructure.repositories.fishers_read_repository.Fisher.objects.get"
    )
    def test_fisher_details_me_raises_repository_error(
        self, mock_fisher_get, fake_user
    ):
        """
        GIVEN a user with an existing fisher profile
        WHEN the repository function is called to fetch the fisher's details
        THEN it raises RepositoryError if a database error occurs"""
        mock_fisher_get.side_effect = DatabaseError()
        with pytest.raises(RepositoryError):
            get_fisher_details_me_repository(user=fake_user)
