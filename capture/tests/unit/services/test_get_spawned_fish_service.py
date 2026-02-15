import pytest
from unittest.mock import patch
from capture.domain.services.capture_fish_service import get_spawned_fish
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher


@pytest.fixture
def user_with_fisher(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )
    Fisher.objects.get_or_create(user=user, nickname=user)
    return user


@pytest.fixture
def user_without_fisher(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )
    return user


@patch(
    "capture.domain.services.capture_fish_service.get_list_fishes_by_habitat_repository"
)
def test_get_spawned_fish_service_returns_data(mock_service, user_with_fisher):
    """
    GIVEN a user with an existing fisher profile and
    a mocked list of fishes for the current zone
    WHEN the get_spawned_fish service is called for that user
    THEN it returns a fish id from the provided list according to rarity weighting
    """
    mock_service.return_value = [{"fish_id": "Catfish", "rarity": "COMMON"}]
    result = get_spawned_fish(user=user_with_fisher)
    assert result in ("Salmon", "Trout", "Catfish", "Catfish", "Pike", "Sturgeon")


@patch(
    "capture.domain.services.capture_fish_service.get_list_fishes_by_habitat_repository"
)
def test_get_spawned_fish_service_raises_fisher_not_found_error(
    mock_service, user_without_fisher
):
    """
    GIVEN a user without an associated fisher profile
    WHEN the get_spawned_fish service is called for that user
    THEN it raises FisherNotFoundError
    """
    mock_service.side_effect = FisherNotFoundError()
    with pytest.raises(FisherNotFoundError):
        get_spawned_fish(user=user_without_fisher)
