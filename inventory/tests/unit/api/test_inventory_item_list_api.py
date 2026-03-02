from rest_framework import status
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, MagicMock
import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from inventory.api.views import InventoryItemListView


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


@pytest.fixture
def api_view():
    return InventoryItemListView.as_view()


ITEM_LIST_PATH = "/inventory/items/"


class TestInventoryItemListSuccess:
    @patch("inventory.api.views.get_inventory_item_list")
    @patch("inventory.api.views.InventoryItemListView.permission_classes", new=[])
    def test_inventory_item_list_api_returns_data(
        self, mock_service, api_request_factory, api_view
    ):
        """
        Given an authenticated user and a mocked inventory service returning items
        When the inventoy item list endpoint is requested
        Then the API responds with HTTP 200 and the expected payload
        """

        fake_user = MagicMock()
        fake_user.is_authenticated = True

        request = api_request_factory.get(path=ITEM_LIST_PATH)
        request.user = fake_user

        mock_service.return_value = [
            {"item_code": "ROD_BASIC", "item_name": "Basic Rod", "quantity": 13},
        ]

        response = api_view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["result"] == mock_service.return_value


class TestInventoryItemListErrors:
    def test_inventory_item_list_api_unauthenticated_user_error(
        self, api_request_factory, api_view
    ):
        """
        Given an unauthenticated client
        When the inventoty item list endpoint is requested
        Then the API responds with HTTP 401 Unauthorized
        """

        fake_user = MagicMock()
        fake_user.is_authenticated = False

        request = api_request_factory.get(path=ITEM_LIST_PATH)
        request.user = fake_user

        response = api_view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("inventory.api.views.get_inventory_item_list")
    @patch("inventory.api.views.InventoryItemListView.permission_classes", new=[])
    def test_inventory_item_list_api_raises_fisher_not_found(
        self, mock_repository, api_request_factory, api_view
    ):
        """
        Given an authenticated user and a mocked inventory service raising FisherNotFoundError
        When the inventoty item list endpoint is requested
        Then the API responds with HTTP 404 Not Found
        """

        mock_repository.side_effect = FisherNotFoundError()

        fake_user = MagicMock()
        fake_user.is_authenticated = True

        request = api_request_factory.get(path=ITEM_LIST_PATH)
        request.user = fake_user

        response = api_view(request)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch("inventory.api.views.get_inventory_item_list")
    @patch("inventory.api.views.InventoryItemListView.permission_classes", new=[])
    def test_inventory_item_list_api_raises_repository_error(
        self, mock_repository, api_request_factory, api_view
    ):
        """
        Given an authenticated user and a mocked inventory service raising RepositoryError
        When the inventoty item list endpoint is requested
        Then the API responds with HTTP 500 Internal Server Error
        """

        mock_repository.side_effect = RepositoryError()

        fake_user = MagicMock()
        fake_user.is_authenticated = True

        request = api_request_factory.get(path=ITEM_LIST_PATH)
        request.user = fake_user

        response = api_view(request)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
