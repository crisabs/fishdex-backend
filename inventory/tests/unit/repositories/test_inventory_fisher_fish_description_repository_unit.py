from unittest.mock import patch
import pytest
from core.exceptions.domain import FisherNotFoundError, FisherFishNotFoundError
from fish.models import Fish
from fishers.models import Fisher
from inventory.infrastructure.repositories.inventory_write_repository import (
    set_description_fisher_fish_repository,
)
from inventory.models import FisherFish


@pytest.fixture
def user_with_fisher_fisherfish(django_user_model):
    """
    Fixture to create a user with an associated fisher fish inventory record for testing.
    This fixture creates a user using the Django user model, along with an associated
    fisher and a fisher fish inventory record.
    The fixture returns the created user
    and the fisher fish inventory record, which can be used
    in test cases to verify the functionality
    of the inventory repositories when a user has an associated fisher fish inventory record.
    """

    user = django_user_model.objects.create_user(
        username="testuser", password="testpassword"
    )
    fish = Fish.objects.get(fish_id=1)
    fisher = Fisher.objects.create(user=user, nickname=user)
    fisherFish = FisherFish.objects.create(
        fisher=fisher, fish=fish, weight=1.0, length=10.0
    )
    return user, fisherFish


@pytest.fixture
def user_with_fisher_without_fisherfish(django_user_model):
    """
    Fixture to create a user with an associated fisher but without
    a fisher fish inventory record for testing.
    This fixture creates a user using the Django user model,
    along with an associated fisher but does not create any fisher fish inventory records.
    The fixture returns the created user,
    which can be used in test cases to verify the functionality
    of the inventory repositories when a user has an associated fisher
    but does not have any fisher fish inventory records.
    """

    user = django_user_model.objects.create_user(
        username="testuser", password="testpassword"
    )
    Fisher.objects.create(user=user, nickname=user)
    return user


@pytest.fixture
def user_without_fisher_without_fisherfish(django_user_model):
    """
    Fixture to create a user without an associated fisher
    and without a fisher fish inventory record for testing.
    This fixture creates a user using the Django user model but does not create any
    associated fisher or fisher fish inventory records. The fixture returns the created user,
    which can be used in test cases to verify the functionality of the inventory repositories
    when a user does not have an associated fisher or any fisher fish inventory records.
    """

    return django_user_model.objects.create_user(
        username="testuser", password="testpassword"
    )


class TestInventoryFisherFishDescriptionRepositorySuccess:
    """
    Test the set_description_fisher_fish_repository function.
    This test verifies that the repository function correctly updates the description
    of a fisher fish inventory record when provided with valid input data.
    It uses a fixture to create a user and an associated fisher fish inventory record,
    then calls the repository function with the user's credentials and the primary key
    of the fisher fish record, along with a new description.
    The test asserts that the repository function returns a success response, indicating
    that the description was updated successfully.
    """

    def test_inventory_fisher_fish_description_repository_success(
        self, user_with_fisher_fisherfish
    ):
        user, fisherFish = user_with_fisher_fisherfish
        result = set_description_fisher_fish_repository(
            user=user, pk=fisherFish.pk, description="A nice fish"
        )
        assert result == {"success": True}


class TestInventoryFisherFishDescriptionRepositoryErrors:
    """
    Test the set_description_fisher_fish_repository function for error cases.
    This test verifies that the repository function raises appropriate exceptions
    when provided with invalid input data, such as a non-existent primary key for the
    fisher fish inventory record or a user that does not have an associated fisher.
    It uses a fixture to create a user and an associated fisher fish inventory record,
    then calls the repository function with invalid input data to trigger the error cases.
    The test asserts that the expected exceptions are raised, indicating that the repository
    function correctly handles error scenarios.
    """

    def test_inventory_fisher_fish_description_repository_invalid_pk(
        self, user_with_fisher_fisherfish
    ):
        user, _ = user_with_fisher_fisherfish
        with pytest.raises(Exception):
            set_description_fisher_fish_repository(
                user=user, pk=9999, description="A nice fish"
            )

    @patch(
        "inventory.infrastructure.repositories.inventory_write_repository.Fisher.objects.get"
    )
    def test_inventory_fisher_fish_description_repository_user_without_fisher(
        self, mock_fisher_get, user_without_fisher_without_fisherfish
    ):
        mock_fisher_get.side_effect = Fisher.DoesNotExist()
        with pytest.raises(FisherNotFoundError):
            set_description_fisher_fish_repository(
                user=user_without_fisher_without_fisherfish,
                pk=1,
                description="A nice fish",
            )

    @patch(
        "inventory.infrastructure.repositories.inventory_write_repository.FisherFish.objects.get"
    )
    def test_inventory_fisher_fish_description_repository_user_with_fisher_without_fisherfish(
        self, mock_fisherfish_get, user_with_fisher_without_fisherfish
    ):
        mock_fisherfish_get.side_effect = FisherFish.DoesNotExist()
        with pytest.raises(FisherFishNotFoundError):
            set_description_fisher_fish_repository(
                user=user_with_fisher_without_fisherfish,
                pk=1,
                description="A nice fish",
            )
