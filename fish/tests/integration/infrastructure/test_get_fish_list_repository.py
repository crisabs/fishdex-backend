from django.db import DatabaseError
import pytest
from fish.infrastructure.repositories.fish_read_repository import (
    get_fish_list_repository,
)
from fish.models import Fish
from unittest.mock import patch
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError


@pytest.mark.django_db
def test_get_fish_list_repository_success():
    """
    GIVEN a Fish record exists in the database
    WHEN get_fish_list_repository is executed
    THEN it returns a list containing the fish data
    """
    Fish.objects.create(
        name="Salmon_test",
        fish_id=111,
        description="A strong migratory fish known for swimming upstream.",
        habitat="RIVER",
        rarity="COMMON",
        base_weight=3.0,
        base_price=15.0,
    )

    result = get_fish_list_repository()
    expected = list(
        Fish.objects.values(
            "id",
            "name",
            "fish_id",
            "description",
            "habitat",
            "rarity",
            "base_weight",
            "base_price",
        )
    )
    assert result == expected


@patch("fish.models.Fish.objects.values")
def test_get_fish_list_repository_fish_does_not_exist(mock_repository):
    """
    GIVEN the Fish repository raises DoesNotExist
    WHEN get_fish_list_repository is executed
    THEN it raises FishesNotFoundInDatabase
    """
    mock_repository.side_effect = Fish.DoesNotExist
    with pytest.raises(FishesNotFoundInDatabase):
        get_fish_list_repository()


@patch("fish.models.Fish.objects.values")
def test_get_fish_list_repository_fish_database_error(mock_repository):
    """
    GIVEN the Fish repository raises DatabaseError
    WHEN get_fish_list_repository is executed
    THEN it raises RepositoryError
    """
    mock_repository.side_effect = DatabaseError
    with pytest.raises(RepositoryError):
        get_fish_list_repository()
