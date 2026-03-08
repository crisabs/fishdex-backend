import pytest

from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from inventory.infrastructure.repositories.inventory_write_repository import (
    set_description_fisher_fish_repository,
)
from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.fisher_fish_factory import FisherFishFactory
from inventory.tests.factories.user_factory import UserFactory


@pytest.fixture
def user_with_fisher_profile_and_fisher_fish(db):
    fisher = FisherFactory()
    fisherFish = FisherFishFactory(fisher=fisher)
    return fisher.user, fisherFish


@pytest.fixture
def user_with_fisher_profile_without_fisher_fish(db):
    fisher = FisherFactory()
    return fisher.user, fisher


@pytest.fixture
def user_without_fisher(db):
    return UserFactory()


class TestInventoryFishDescriptionIntegrationSuccess:
    def test_fish_description_integration_returns_data(
        self, user_with_fisher_profile_and_fisher_fish
    ):
        """
        GIVEN a valid user and valid inventory primary key
        WHEN the set_description_fisher_fish_repository is called
        THEN the repository returns a success response with the updated description
        """
        user, fisherFish = user_with_fisher_profile_and_fisher_fish
        result = set_description_fisher_fish_repository(
            user=user, pk=fisherFish.pk, description="This fish was my first fish"
        )
        assert result["success"] is True


class TestInventoryFishDescriptionIntegrationErrors:
    def test_fish_description_integration_raises_fisher_not_found(
        self, user_without_fisher
    ):
        """
        GIVEN a valid user but the repository cannot find the associated fisher
        WHEN the set_description_fisher_fish_repository is called
        THEN the repository propagates the FisherNotFoundError from the repository
        """
        user = user_without_fisher
        with pytest.raises(FisherNotFoundError) as exc:
            set_description_fisher_fish_repository(
                user=user, pk=1, description="This fish was my second fish"
            )
        assert str(exc.value) == FisherNotFoundError.default_detail

    def test_fish_description_integration_raises_fisherfish_not_found(
        self, user_with_fisher_profile_without_fisher_fish
    ):
        """
        GIVEN a valid user but the repository cannot find the fisher fish inventory record
        WHEN the set_description_fisher_fish_repository is called
        THEN the repository propagates the FisherFishNotFoundError from the repository
        """
        user, _ = user_with_fisher_profile_without_fisher_fish
        with pytest.raises(FisherFishNotFoundError) as exc:
            set_description_fisher_fish_repository(
                user=user, pk=55, description="This fish was my second fish"
            )
        assert str(exc.value) == FisherFishNotFoundError.default_detail

    @pytest.mark.django_db(
        transaction=True
    )  # Ensure that the test runs in a transaction to properly test database errors
    def test_fish_description_integration_raises_repository_error(
        self, user_with_fisher_profile_and_fisher_fish
    ):
        """
        GIVEN a valid user and valid inventory primary key but a database error occurs
        WHEN the set_description_fisher_fish_repository is called
        THEN the repository propagates the RepositoryError from the repository

        Note: This test simulates a database error by providing an excessively long description
        that exceeds the maximum length defined in the model,
        which should trigger a database-level error.

        The test is marked with @pytest.mark.django_db(transaction=True) to ensure it runs within
        """
        user, fisherFish = user_with_fisher_profile_and_fisher_fish
        with pytest.raises(RepositoryError) as exc:
            set_description_fisher_fish_repository(
                user=user, pk=fisherFish.pk, description="X" * 300
            )
        assert str(exc.value) == RepositoryError.default_detail
