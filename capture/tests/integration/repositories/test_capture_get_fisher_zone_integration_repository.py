from capture.infrastructure.repositories.capture_read_repository import (
    get_fisher_zone_repository,
)
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher
import pytest


@pytest.fixture
def user_with_fisher(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )
    Fisher.objects.create(user=user, nickname=user)
    return user


@pytest.fixture
def user_without_fisher(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )


def test_capture_get_fisher_zone_integration_repository_success(user_with_fisher):
    """
    GIVEN an authenticated user with an associated Fisher profile
    WHEN the fisher zone is retrieved from the repository
    THEN the repository returns a valid fishing zone.
    """
    result = get_fisher_zone_repository(user=user_with_fisher)
    assert result in ("RIVER", "LAKE", "OCEAN")


def test_capture_get_fisher_zone_integration_repository_fisher_not_found_error(
    user_without_fisher,
):
    """
    GIVEN an authenticated user without a Fisher profile
    WHEN the fisher zone is requested from the repository
    THEN a FisherNotFoundError is raised with the expected error code.
    """

    with pytest.raises(FisherNotFoundError) as exc_info:
        get_fisher_zone_repository(user=user_without_fisher)

    assert exc_info.value.default_code == FisherNotFoundError.default_code
