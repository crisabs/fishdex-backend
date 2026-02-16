from capture.infrastructure.repositories.capture_read_repository import (
    get_list_fishes_by_habitat_repository,
)
import pytest


@pytest.mark.django_db
def test_capture_get_list_fishes_by_habitat_integration_repository_success():
    """
    GIVEN a habitat with fishes stored in the database
    WHEN the fishes are retrieved from the repository for that habitat
    THEN the repository returns a list of fishes with their IDs and rarity
    """
    test_habitat = "RIVER"
    expected_result = [
        {"fish_id": 1, "rarity": "COMMON"},
    ]
    result = get_list_fishes_by_habitat_repository(habitat=test_habitat)
    assert result[0] == expected_result[0]


@pytest.mark.django_db
def test_get_list_fishes_by_habitat_integration_repository_returns_empty_list():
    """
    GIVEN a habitat with no fishes stored in the database
    WHEN the fishes are retrieved from the repository for that habitat
    THEN the repository returns an empty list
    """
    test_habitat = "SEA"
    result = get_list_fishes_by_habitat_repository(habitat=test_habitat)
    assert result == []
