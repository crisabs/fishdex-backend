from rest_framework.test import APIRequestFactory
from rest_framework import status
import pytest
from unittest.mock import patch, MagicMock
from core.exceptions.bd import RepositoryError
from inventory.api.views import InventoryFisherFishDescriptionView


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


@pytest.fixture
def api_view():
    return InventoryFisherFishDescriptionView.as_view()


@pytest.fixture
def request_data():
    return {"pk": 1, "description": "A custom inventory fish description"}


FISHER_FISH_DESCRIPTION_PATH = "/fisher-fish-description/"


class TestInventoryFisherFishSuccess:

    @patch("inventory.api.views.set_description_fisher_fish")
    @patch(
        "inventory.api.views.InventoryFisherFishDescriptionView.permission_classes",
        new=[],
    )
    def test_set_description_fisher_fish_success_returns_data(
        self, mock_service, api_request_factory, api_view, request_data
    ):
        """
        GIVEN a valid request to set the description of a fisher fish inventory record
        WHEN the request is processed
        THEN the service function should be called with
        the correct parameters and a successful response should be returned
        """
        mock_service.return_value = {"success": True}
        fake_user = MagicMock()
        fake_user.is_authenticated = True

        request = api_request_factory.patch(
            path=FISHER_FISH_DESCRIPTION_PATH, data=request_data, format="json"
        )
        request.user = fake_user

        response = api_view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True


class TestInventoryFisherFishErrors:
    def test_set_description_fisher_fish_unauthenticated_returns_401(
        self, api_request_factory, api_view, request_data
    ):
        """
        GIVEN an unauthenticated request to set the description
        of a fisher fish inventory record
        WHEN the request is processed
        THEN a 401 Unauthorized response should be returned"""

        fake_user = MagicMock()
        fake_user.is_authenticated = False

        request = api_request_factory.patch(
            path=FISHER_FISH_DESCRIPTION_PATH, data=request_data, format="json"
        )
        request.user = fake_user
        response = api_view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("inventory.api.views.set_description_fisher_fish")
    @patch(
        "inventory.api.views.InventoryFisherFishDescriptionView.permission_classes",
        new=[],
    )
    def test_set_description_fisher_fish_invalid_data_returns_400(
        self, mock_service, api_request_factory, api_view
    ):
        """
        GIVEN an authenticated request with invalid data to set the description
        of a fisher fish inventory record
        WHEN the request is processed
        THEN a 400 Bad Request response should be returned
        """
        fake_user = MagicMock()
        fake_user.is_authenticated = True

        mock_service.side_effect = RepositoryError()

        request_invalid_data = {"pk": "invalid_pk", "description": 123}
        request = api_request_factory.patch(
            path=FISHER_FISH_DESCRIPTION_PATH, data=request_invalid_data, format="json"
        )
        request.user = fake_user
        response = api_view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
