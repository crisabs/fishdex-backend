from unittest.mock import patch

import pytest
from fish.domain.services.fish_service import get_fish_list
from core.exceptions.bd import RepositoryError


@patch("fish.domain.services.fish_service.get_fish_list_repository")
def test_service_get_fish_list_returns_data(mock_repository):
    """
    GIVEN the fish repository returns a list of fish entities
    WHEN the get_fish_list service is executed
    THEN it returns the same list of fish dictionaries
    """
    mock_repository.return_value = [
        {
            "id": 9,
            "name": "Salmon",
            "fish_id": 1,
            "description": "A strong migratory fish known for swimming upstream.",
            "habitat": "RIVER",
            "rarity": "COMMON",
            "base_weight": 3.0,
            "base_price": 15.0,
        },
    ]
    result = get_fish_list()
    assert result == mock_repository.return_value
    mock_repository.assert_called_once()


@pytest.mark.django_db
@patch("fish.domain.services.fish_service.get_fish_list_repository")
def test_service_get_fish_list_repository_error(mock_repository):
    """
    GIVEN the fish repository raises a RepositoryError
    WHEN the get_fish_list service is executed
    THEN the RepositoryError is propagated
    """
    mock_repository.side_effect = RepositoryError
    with pytest.raises(RepositoryError):
        get_fish_list()
