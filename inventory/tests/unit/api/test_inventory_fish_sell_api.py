import pytest
from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import patch, MagicMock
from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from inventory.api.views import InventoryFishSellAPIView
from rest_framework.response import Response


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.fixture
def api_view():
    return InventoryFishSellAPIView.as_view()


@pytest.fixture
def request_data():
    return {
        "fish_id": 1,
        "total_weight": 2,
        "pk": 10,
    }


class TestInventoryFishSellSuccess:
    @patch("inventory.api.views.InventoryFishSellAPIView.permission_classes", new=[])
    @patch("inventory.api.views.sell_fish")
    def test_sell_fish_success(
        self, mock_sell_fish, api_factory, api_view, request_data
    ):
        """
        GIVEN a valid request to sell a fish
        WHEN the request is made to the inventory fish sell endpoint
        THEN the fish is sold successfully and a 200 OK response is returned
        """
        fake_user = MagicMock()
        fake_user.is_authenticated = True

        mock_sell_fish.return_value = {
            "code": "OK",
        }

        request = api_factory.post(
            path="/inventory/fish-sell/", data=request_data, format="json"
        )
        request.user = fake_user

        response = api_view(request)

        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data["code"] == mock_sell_fish.return_value["code"]


class TestInventoryFishSellErrors:
    def test_sell_fish_unauthenticated(self, api_factory, api_view, request_data):
        """
        GIVEN an unauthenticated request to sell a fish
        WHEN the request is made to the inventory fish sell endpoint
        THEN a 401 Unauthorized response is returned
        """
        fake_user = MagicMock()
        fake_user.is_authenticated = False

        request = api_factory.post(
            path="/inventory/fish-sell/", data=request_data, format="json"
        )
        request.user = fake_user
        response = api_view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("inventory.api.views.sell_fish")
    @patch("inventory.api.views.InventoryFishSellAPIView.permission_classes", new=[])
    def test_sell_fish_fisher_not_found(
        self, mock_service, api_factory, api_view, request_data
    ):
        """
        GIVEN a mocked authenticated user and the inventory fish sell
        service mocked to raise a FisherNotFoundError.
        WHEN The authenticated user sends a POST request to the inventory fish sell endpoint.
        THEN The API responds with HTTP 404 Not Found and the error message from the exception.
        """
        fake_user = MagicMock()
        fake_user.is_authenticated = True

        mock_service.side_effect = FisherNotFoundError()
        request = api_factory.post(
            path="/inventory/fish-sell/", data=request_data, format="json"
        )
        request.user = fake_user
        response = api_view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert isinstance(response, Response)
        assert response.data is not None
        assert response.data["detail"] == FisherNotFoundError.default_detail

    @patch("inventory.api.views.sell_fish")
    @patch("inventory.api.views.InventoryFishSellAPIView.permission_classes", new=[])
    def test_sell_fish_fisher_fish_not_found(
        self, mock_service, api_factory, api_view, request_data
    ):
        """
        GIVEN a valid request to sell a fish but the fisher fish is not found
        WHEN the request is made to the inventory fish sell endpoint
        THEN a 404 Not Found response is returned with the appropriate error message"""

        fake_user = MagicMock()
        fake_user.is_authenticated = True

        mock_service.side_effect = FisherFishNotFoundError()

        request = api_factory.post(
            path="/inventory/fish-sell/", data=request_data, format="json"
        )
        request.user = fake_user
        response = api_view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == FisherFishNotFoundError.default_detail
