from unittest.mock import patch

import pytest
from fish.domain.services.fish_service import get_fish_details
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError


@patch("fish.domain.services.fish_service.get_fish_details_repository")
def test_service_get_fish_details_sucess(mock_repository):
    """
    GIVEN the repository returns valid fish data for a given fish_id
    WHEN the get_fish_defails service is called
    THEN it should return the fish data without modification
    """
    mock_repository.return_value = {
        "fish_id": 9,
        "name": "fish_name",
        "description": "fish_description",
        "habitat": "fish_habitat",
        "rarity": "fish_rarity",
        "base_weight": 0.4,
        "base_price": 0.5,
    }
    test_fish_id = 9
    result = get_fish_details(fish_id=test_fish_id)
    assert result["fish_id"] == 9
    assert result["name"] == "fish_name"


@pytest.mark.django_db
@patch("fish.domain.services.fish_service.get_fish_details_repository")
def test_service_get_fish_details_fishes_not_found_in_db(mock_repository):
    """
    GIVEN the repository raises FishesNotFoundInDatabase
    WHEN the get_fish_details service is called
    THEN the exception should be propagated to the caller
    """
    test_fish_id = 9
    mock_repository.side_effect = FishesNotFoundInDatabase
    with pytest.raises(FishesNotFoundInDatabase):
        get_fish_details(fish_id=test_fish_id)


@pytest.mark.django_db
@patch("fish.domain.services.fish_service.get_fish_details_repository")
def test_service_get_fish_details_repository_error(mock_repository):
    """
    GIVEN the repository raises RepositoryError
    WHEN the get_fish_details service is called
    THEN the exception should be prapagated to the caller
    """
    test_fish_id = 9
    mock_repository.side_effect = RepositoryError
    with pytest.raises(RepositoryError):
        get_fish_details(fish_id=test_fish_id)
