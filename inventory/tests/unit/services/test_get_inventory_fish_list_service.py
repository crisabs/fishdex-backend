from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher
from inventory.domain.services.inventory_service import get_inventory_fish_list
from unittest.mock import patch
import pytest


@pytest.fixture
def user_with_fisher_profile(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )
    Fisher.objects.create(user=user, nickname=user)
    return user


@pytest.fixture
def user_without_fisher_profile(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )


@patch("inventory.domain.services.inventory_service.get_inventory_fish_list_repository")
def test_get_inventory_fish_list_service_returns_data(
    mock_repository, user_with_fisher_profile
):
    """
    GIVEN a user with fisher profile
    AND a mocked repository returning a list of fishes
    WHEN get_inventory_fish_list is called
    THEN it should return a list of fishes with calculated price and expected fields
    """
    mock_repository.return_value = [
        {
            "fish__name": "Salmon",
            "fish__base_price": 15,
            "weight": 0.3,
            "caught_at": "2026-02-10T05:52:57.267600Z",
            "fish__rarity": "COMMON",
        },
    ]

    expected_result = [
        {
            "fish_name": "Salmon",
            "price": 4,
            "weight": 0.3,
            "caught_at": "2026-02-10T05:52:57.267600Z",
            "rarity": "COMMON",
        }
    ]
    result = get_inventory_fish_list(user=user_with_fisher_profile)
    assert result == expected_result


@patch("inventory.domain.services.inventory_service.get_inventory_fish_list_repository")
def test_get_inventory_fish_list_service_raises_fisher_not_found_error(
    mock_repository, user_without_fisher_profile
):
    """
    GIVEN a user without a fisher profile
    AND a mocked repository raising FisherNotFoundError
    WHEN get_inventory_fish_list is called
    THEN it should raise FisherNotFoundError
    """

    mock_repository.side_effect = FisherNotFoundError()

    with pytest.raises(FisherNotFoundError):
        get_inventory_fish_list(user=user_without_fisher_profile)


@patch("inventory.domain.services.inventory_service.get_inventory_fish_list_repository")
def test_get_inventory_fish_list_service_raises_repository_error(
    mock_repository, user_with_fisher_profile
):
    """
    GIVEN a user with a fisher profile
    AND a mocked repository raising RepositoryError
    WHEN get_inventory_fish_list is called
    THEN it should raise RepositoryError
    """

    mock_repository.side_effect = RepositoryError()

    with pytest.raises(RepositoryError):
        get_inventory_fish_list(user=user_with_fisher_profile)
