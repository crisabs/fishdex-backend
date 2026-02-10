from unittest.mock import patch

import pytest
from capture.domain.services.capture_fish_service import capture_fish_service
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@user.com", password="user_test"
    )


@patch("capture.domain.services.capture_fish_service.capture_fish_repository")
def test_capture_fish_service_success_returns_data(mock_repository, user):
    """
    GIVEN a valid user and a fish capture request
    WHEN capture_fish_service is excecuted
    THEN it returns a result indicating either success or escape of the fish
    """
    rod_code = "ROD_BASIC"
    bait_code = "BAIT_BASIC"
    fish_id = 1
    fish_weight = 0.1
    fish_length = 1.2

    expected_result_captured = {"captured": True, "message": "Fish captured!"}
    expected_result_escaped = {"captured": False, "message": "The fish escaped"}

    result = capture_fish_service(
        user=user,
        rod_code=rod_code,
        bait_code=bait_code,
        fish_id=fish_id,
        fish_weight=fish_weight,
        fish_length=fish_length,
    )

    assert result in (expected_result_captured, expected_result_escaped)


@patch("capture.domain.services.capture_fish_service.random.random")
@patch("capture.domain.services.capture_fish_service.capture_fish_repository")
def test_capture_fish_service_raises_fisher_not_found_error(
    mock_repository, mock_random, user
):
    """
    GIVEN a user with no associtated Fisher
    WHEN capture_fish_service attempts to presist a captured fish
    THEN it raises a FisherNotFoundError
    """
    mock_random.return_value = 0.0

    rod_code = "ROD_SUPER"
    bait_code = "BAIT_SUPER"
    fish_id = 1
    fish_weight = 0.1
    fish_length = 1.2

    mock_repository.side_effect = FisherNotFoundError()
    with pytest.raises(FisherNotFoundError):

        capture_fish_service(
            user=user,
            rod_code=rod_code,
            bait_code=bait_code,
            fish_id=fish_id,
            fish_weight=fish_weight,
            fish_length=fish_length,
        )


@patch("capture.domain.services.capture_fish_service.random.random")
@patch("capture.domain.services.capture_fish_service.capture_fish_repository")
def test_capture_fish_service_raises_repository_error(
    mock_repository, mock_random, user
):
    """
    GIVEN a user and a fish capture request where presistence fails
    WHEN capture_fish_service attempts to persist the capture
    THEN it raises a RepositoryError
    """

    rod_code = "ROD_ULTRA"
    bait_code = "BAIT_ULTRA"
    fish_id = 1
    fish_weight = 0.00001
    fish_length = 1.2

    mock_random.return_value = 0.0
    mock_repository.side_effect = RepositoryError()
    with pytest.raises(RepositoryError):

        capture_fish_service(
            user=user,
            rod_code=rod_code,
            bait_code=bait_code,
            fish_id=fish_id,
            fish_weight=fish_weight,
            fish_length=fish_length,
        )
