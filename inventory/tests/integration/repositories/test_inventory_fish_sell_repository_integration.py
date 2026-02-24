from unittest.mock import patch, Mock
from django.db import DatabaseError
import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from fish.models import Fish
from fishers.models import Fisher
from inventory.infrastructure.repositories.inventory_write_repository import (
    sell_fish_repository,
)
from inventory.models import FisherFish
from inventory.tests.factories.user_factory import (
    build_test_email,
    build_test_nickname,
    build_test_password,
)


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username=build_test_email(), password=build_test_password()
    )


@pytest.fixture
def fisher(db, user):
    return Fisher.objects.create(user=user, nickname=build_test_nickname())


@pytest.fixture
def fish(db):
    fish, _ = Fish.objects.get_or_create(fish_id=1, defaults={"name": "Salmon"})
    return fish


@pytest.mark.django_db
class TestFishSellRepositoryIntegrationSuccess:
    def test_sell_fish_success(self, user, fisher, fish):
        """
        GIVEN a user with a fisher profile and a fisher fish
        WHEN the sell_fish_repository is called with valid parameters
        THEN the fisher fish is deleted and the fisher's coins are updated
        """
        FisherFish.objects.create(fisher=fisher, fish=fish, weight=10, length=1)

        pk = (
            FisherFish.objects.filter(fisher=fisher)
            .select_related("fish")
            .values_list("pk", flat=True)
            .first()
        )
        result = sell_fish_repository(user=user, pk=pk, total_price=1)
        assert result["code"] == "OK"


class TestFishSellRepositoryIntegrationErrors:
    @patch(
        "inventory.infrastructure.repositories.inventory_write_repository.FisherFish.objects.select_for_update"
    )
    def test_sell_fish_repository_error(
        self, mock_select_for_update, user, fisher, fish
    ):
        """GIVEN a user with a fisher profile and a fisher fish
        WHEN the sell_fish_repository is called and a DatabaseError occurs
        THEN a RepositoryError is raised
        """

        mock_qs = Mock()
        mock_qs.get.side_effect = DatabaseError()
        mock_select_for_update.return_value = mock_qs

        with pytest.raises(RepositoryError) as exc:
            sell_fish_repository(user=user, pk=1, total_price=1)
            assert str(exc.value.default_detail) == RepositoryError.default_detail

    def test_sell_fisher_fish_not_found_error(self, user, fisher):
        """
        GIVEN a user with a fisher profile and a fisher fish
        WHEN the sell_fish_repository is called with a non-existent fisher fish pk
        THEN a FisherFishNotFoundError is raised
        """
        with pytest.raises(FisherFishNotFoundError):
            sell_fish_repository(user=user, pk=200, total_price=1)

    def test_sell_fisher_not_found_error(self, user):
        """
        GIVEN a user without a fisher profile
        WHEN the sell_fish_repository is called with valid parameters
        THEN a FisherNotFoundError is raised
        """
        user = user
        with pytest.raises(FisherNotFoundError):
            sell_fish_repository(user=user, pk=1, total_price=1)
