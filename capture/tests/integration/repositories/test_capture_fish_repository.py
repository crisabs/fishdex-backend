from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher
from inventory.models import FisherFish
import pytest
from unittest.mock import patch
from capture.infrastructure.repositories.capture_write_repository import (
    capture_fish_repository,
)


@pytest.fixture
def user_with_fisher(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@test.conm", password="user_test"
    )
    Fisher.objects.create(user=user, nickname=user)
    return user


@pytest.fixture
def user_without_fisher(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@test.conm", password="user_test"
    )
    Fisher.objects.create(user=user, nickname=user)
    return user


@pytest.mark.django_db
def test_capture_fish_repository_success(user_with_fisher):
    """
    GIVEN a user with an associated fisher and valid fish data.
    WHEN the capture fish repository is called with valid parameters.
    THEN A FisherFish record is created with the expected fish, weight, and length.
    """
    capture_fish_repository(
        user=user_with_fisher, fish_id=1, fish_weight=1, fish_length=1
    )
    fisherFish = FisherFish.objects.get(fisher__user=user_with_fisher)

    assert fisherFish.fish.fish_id == 1
    assert fisherFish.weight == 1
    assert fisherFish.length == 1


@patch(
    "capture.infrastructure.repositories.capture_write_repository.Fisher.objects.get"
)
def test_capture_fish_repository_raises_fisher_not_found_error(
    mock_fisher, user_without_fisher
):
    """
    GIVEN A user without a valid fisher associated in the system.
    WHEN The capture fish repository attempts to retrive the fisher.
    THEN A FisherNotFoundError is raised.
    """
    mock_fisher.side_effect = FisherNotFoundError()
    with pytest.raises(FisherNotFoundError):
        capture_fish_repository(
            user=user_without_fisher, fish_id=1, fish_weight=1, fish_length=1
        )


@patch("capture.infrastructure.repositories.capture_write_repository.Fish.objects.get")
def test_capture_fish_repository_raises_fishes_not_found_in_database(
    mock_fish, user_with_fisher
):
    """
    GIVEN A valid user with an associated fisher.
    WHEN The capture fish repository fails to find the fish in the database.
    THEN A FishesNotFoundInDatabase exception is raised.
    """
    mock_fish.side_effect = FishesNotFoundInDatabase()
    with pytest.raises(FishesNotFoundInDatabase):
        capture_fish_repository(
            user=user_with_fisher, fish_id=1, fish_weight=1, fish_length=1
        )


@patch("capture.infrastructure.repositories.capture_write_repository.FisherFish.save")
def test_capture_fish_repository_raises_repository_error(
    mock_fisher_fish, user_with_fisher
):
    """
    GIVEN a valir user, fisher and fish.
    WHEN persisting the FisherFish entity fails at the repository level.
    THEN A RepositoryError is raised.
    """
    mock_fisher_fish.side_effect = RepositoryError()
    with pytest.raises(RepositoryError):
        capture_fish_repository(
            user=user_with_fisher, fish_id=1, fish_weight=1, fish_length=1
        )
