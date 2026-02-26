# from unittest.mock import patch
import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from inventory.domain.services.inventory_service import (
    set_description_fisher_fish,
)
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory
from inventory.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher_and_fisher_fish(db):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)

    return fisher.user, fisherFish


@pytest.fixture
def user_without_fisher(db):
    return UserFactory()


class TestFisherFishDescriptionServiceSuccess:

    def test_set_description_updates_fisher_fish_successfully(
        self, user_with_fisher_and_fisher_fish
    ):
        """
        GIVEN a user with a fisher and a fisher fish
        WHEN set_description_fisher_fish is called with valid data
        THEN the fisher fish's description is updated successfully"""
        user, fisherFish = user_with_fisher_and_fisher_fish
        response = set_description_fisher_fish(
            user=user,
            pk=fisherFish.pk,
            description="New description",
        )
        assert response == {"success": True}


class TestFisherFishDescriptionServiceErrors:

    def test_set_description_fisher_fish_raises_fisher_not_found(
        self, user_without_fisher
    ):
        """
        GIVEN a user without a fisher
        WHEN set_description_fisher_fish is called
        THEN a FisherNotFoundError is raised
        """
        with pytest.raises(FisherNotFoundError) as exc_info:
            set_description_fisher_fish(
                user=user_without_fisher,
                pk=1,
                description="New description",
            )
        assert str(exc_info.value) == FisherNotFoundError.default_detail

    def test_set_description_fisher_fish_raises_repository_error(
        self, user_with_fisher_and_fisher_fish
    ):
        """
        GIVEN a user with a fisher and a fisher fish
        WHEN set_description_fisher_fish is called with an invalid description
        THEN a RepositoryError is raised
        """
        with pytest.raises(RepositoryError) as exc_info:
            user, fisherFish = user_with_fisher_and_fisher_fish
            set_description_fisher_fish(
                user=user,
                pk=fisherFish.pk,
                description="x" * 55,
            )
        assert str(exc_info.value) == RepositoryError.default_detail
