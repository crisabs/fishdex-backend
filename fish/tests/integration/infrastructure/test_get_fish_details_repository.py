from django.db import DatabaseError
import pytest
from unittest.mock import patch
from fish.infrastructure.repositories.fish_read_repository import (
    get_fish_details_repository,
)

from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError
from fish.models import Fish


@pytest.mark.django_db
def test_get_fish_details_repository_success():
    """
    GIVEN a fish stored in the database
    WHEN the fish details are requested by fish_id
    THEN the repository returns the complete fish information.
    """

    test_fish_id = 999
    test_fish_name = "Test Largemouth Bass"

    Fish.objects.create(
        fish_id=test_fish_id,
        name=test_fish_name,
        description="A popular sport fish with powerful strikes.",
        habitat="LAKE",
        rarity="RARE",
        base_weight=3.5,
        base_price=30.0,
    )

    expected_result = {
        "fish_id": test_fish_id,
        "name": test_fish_name,
        "description": "A popular sport fish with powerful strikes.",
        "habitat": "LAKE",
        "rarity": "RARE",
        "base_weight": 3.5,
        "base_price": 30.0,
    }

    result = get_fish_details_repository(fish_id=test_fish_id)
    assert result["fish_id"] == test_fish_id
    assert result["name"] == test_fish_name
    assert result == expected_result


@pytest.mark.django_db
@patch("fish.infrastructure.repositories.fish_read_repository.Fish.objects.get")
def test_get_fish_details_repository_fishes_not_found_in_db(mock_db_model):
    """
    GIVEN a fish that does not exist in the database
    WHEN the fish details are requested by fish_id
    THEN a FishesNotFoundInDabatase exception is raised.
    """
    mock_db_model.side_effect = Fish.DoesNotExist
    test_fish_id = 999
    with pytest.raises(FishesNotFoundInDatabase):
        get_fish_details_repository(fish_id=test_fish_id)


@pytest.mark.django_db
@patch("fish.infrastructure.repositories.fish_read_repository.Fish.objects.get")
def test_get_fish_details_repository_repository_error(mock_db_model):
    """
    GIVEN a database access error
    WHEN the fish details are requested by fish_id
    THEN a RepositoryError exception is raised.
    """
    mock_db_model.side_effect = DatabaseError
    test_fish_id = 999
    with pytest.raises(RepositoryError):
        get_fish_details_repository(fish_id=test_fish_id)
