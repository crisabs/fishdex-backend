from unittest.mock import patch
from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher
import pytest
from inventory.domain.services.inventory_service import (
    get_inventory_fish_list_repository,
)


@pytest.fixture
def user_with_fisher(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )
    fisher = Fisher.objects.create(user=user, nickname=user)
    return user, fisher


@pytest.fixture
def user_without_fisher(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )


@pytest.mark.unit
@pytest.mark.django_db
@patch(
    "inventory.infrastructure.repositories.inventory_read_repository.Fisher.objects.get"
)
def test_inventory_fish_list_repository_raises_fisher_not_found_error_unit(
    mock_fisher_model, user_without_fisher
):
    """
    GIVEN a user without an associated Fisher profile
    WHEN the repository tries to retrive the Fisher for the user
    and the ORM raises Fisher.DoesNotExist
    THEN the repository should translate the exception and raise FisherNotFoundError
    """
    user = user_without_fisher
    mock_fisher_model.side_effect = Fisher.DoesNotExist
    with pytest.raises(FisherNotFoundError):
        get_inventory_fish_list_repository(user=user)


@pytest.mark.unit
@pytest.mark.django_db
@patch(
    "inventory.infrastructure.repositories.inventory_read_repository.FisherFish.objects.filter"
)
def test_inventory_fish_list_repository_raises_repository_error_unit(
    mock_db, user_with_fisher
):
    """
    GIVEN a user with an associated Fisher profile
    WHEN the repository tries to fetch inventory fishes
    and the ORM raises a DatabaseError
    THEN the repository should translate the exception and raise RepositoryError
    """

    user, _ = user_with_fisher

    mock_db.side_effect = DatabaseError()
    with pytest.raises(RepositoryError):
        get_inventory_fish_list_repository(user=user)
