from rest_framework import status
from unittest.mock import patch, MagicMock
from rest_framework.test import APIRequestFactory
from core.exceptions.domain import FisherNotFoundError
from inventory.api.views import InventoryFishListView
from rest_framework.response import Response
import pytest


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.fixture
def fish_list_view():
    return InventoryFishListView.as_view()


class TestInventoryFisherFishListSuccess:

    @patch("inventory.api.views.InventoryFishListView.permission_classes", new=[])
    @patch("inventory.api.views.get_inventory_fish_list")
    def test_inventory_fish_list_api_returns_data(
        self, mock_service, api_factory, fish_list_view
    ):
        """
        GIVEN An mocked authenticated user and the inventory fish service mocked
        to return a valid fish list.
        WHEN The authenticated user sends a GET request to the inventory fish list endpoit.
        THEN The API responds with HTTP 200, a successful flag,
        and the expected list of fishes serialized according to the API contract.
        """
        fake_user = MagicMock()
        fake_user.is_authenticated = True

        mock_service.return_value = [
            {
                "fish_name": "Salmon",
                "price": 4,
                "pk": 1,
                "weight": "0.30",
                "caught_at": "2026-02-10T05:52:57.267600Z",
                "rarity": "COMMON",
            },
        ]

        request = api_factory.get("/inventory/fishes/")
        request.user = fake_user
        response = fish_list_view(request)

        assert isinstance(response, Response)
        assert response.data is not None

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["result"] == mock_service.return_value


class TestInventoryFisherListErrors:
    def test_inventory_fish_list_api_unauthenticated_user(
        self, api_factory, fish_list_view
    ):
        """
        GIVEN An mocked unauthenticated client.
        WHEN the client sends a GET request to the inventory fish list endpoint.
        THEN the API responds with HTTP 401 Unauthorized.
        """

        fake_user = MagicMock()
        fake_user.is_authenticated = False

        request = api_factory.get("/inventory/fishes/")
        request.user = fake_user

        response = fish_list_view(request)

        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("inventory.api.views.get_inventory_fish_list")
    @patch("inventory.api.views.InventoryFishListView.permission_classes", new=[])
    def test_inventory_fish_list_api_raises_fisher_not_found(
        self, mock_service, api_factory, fish_list_view
    ):
        """
        GIVEN An mocked authenticated user and the inventory fish
        service mocked to raise a FisherNotFoundError.
        WHEN The authenticated user sends a GET request to the inventory fish list endpoint.
        THEN The API responds with HTTP 404 Not Found and the error message from the exception.
        """
        mock_service.side_effect = FisherNotFoundError()

        fake_user = MagicMock()
        fake_user.is_authenticated = True

        request = api_factory.get("/inventory/fishes/")
        request.user = fake_user

        response = fish_list_view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert isinstance(response, Response)
        assert response.data is not None
        assert response.data["detail"] == FisherNotFoundError.default_detail
