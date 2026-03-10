import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.domain.services.fishers_service import set_fisher_nickname
from fishers.tests.factories.fisher_factory import FisherFactory
from fishers.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher(db):
    fisher = FisherFactory()
    return fisher.user


@pytest.fixture
def user_without_fisher(db):
    return UserFactory()


class TestSetFishersNicknameSuccess:
    def test_set_fishers_nickname_returns_data(self, user_with_fisher):
        """
        GIVEN a user with a corresponding Fisher profile
        WHEN set_fisher_nickname is called with that user and a new nickname
        THEN it returns a confirmation message with the new nickname
        """
        result = set_fisher_nickname(user=user_with_fisher, nickname="fake_nickname")
        assert result == "Fisher nickname updated to fake_nickname"


class TestSetFishersNicknameErrors:
    def test_set_fishers_nickname_raises_fisher_not_found(self, user_without_fisher):
        """
        GIVEN a user without a corresponding Fisher profile
        WHEN set_fisher_nickname is called with that user and a new nickname
        THEN it raises a FisherNotFoundError
        """
        with pytest.raises(FisherNotFoundError):
            set_fisher_nickname(user=user_without_fisher, nickname="fake_nickname")

    def test_set_fishers_nickname_raises_repository_error(self, user_with_fisher):

        invalid_nickname = "x" * 500
        with pytest.raises(RepositoryError):
            set_fisher_nickname(user=user_with_fisher, nickname=invalid_nickname)
