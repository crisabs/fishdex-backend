import pytest
from unittest.mock import MagicMock, patch
from fishers.api.views import FisherChangeZoneAPIView
from rest_framework.test import APIRequestFactory
from rest_framework import status

API_PATH = "/fishers/change-zone/"


@pytest.fixture
def authenticated_user_with_coins():
    fake_user = MagicMock(coins=1500)
    fake_user.is_authenticated = True
    return fake_user


@pytest.fixture
def authenticated_user_without_coins():
    fake_user = MagicMock(coins=0)
    fake_user.is_authenticated = True
    return fake_user


@pytest.fixture
def unauthenticated_user_with_coins():
    fake_user = MagicMock(coins=1000)
    fake_user.is_authenticated = False
    return fake_user


@pytest.fixture
def api_view():
    return FisherChangeZoneAPIView.as_view()


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


class TestFisherChangeZoneSuccess:
    @patch("fishers.api.views.FisherChangeZoneAPIView.permission_classes", new=[])
    @patch("fishers.api.views.set_fisher_zone")
    def test_fisher_change_zone_returns_data(
        self, service_mock, authenticated_user_with_coins, api_request_factory, api_view
    ):
        """
        GIVEN an authenticated user with coins
        WHEN the user successfully changes their zone
        THEN the API returns a 200 OK response with the new zone information"""
        payload = {"new_zone": "LAKE"}
        service_mock.return_value = {
            "code": "ZONE_CHANGED",
            "new_zone": payload["new_zone"],
        }

        request = api_request_factory.patch(API_PATH, data=payload, format="json")
        request.user = authenticated_user_with_coins

        response = api_view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == service_mock.return_value["code"]
        assert response.data["new_zone"] == service_mock.return_value["new_zone"]

        service_mock.assert_called_once_with(request.user, new_zone=payload["new_zone"])


class TestFisherChangeZoneErrors:

    def test_fisher_change_zone_unauthenticated_user(
        self, unauthenticated_user_with_coins, api_request_factory, api_view
    ):
        """
        GIVEN an unauthenticated user with coins
        WHEN the user attempts to change their zone
        THEN the API returns a 401 Unauthorized response due to lack of authentication
        """
        payload = {"new_zone": "LAKE"}

        request = api_request_factory.patch(path=API_PATH, data=payload, format="json")
        request.user = unauthenticated_user_with_coins

        response = api_view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("fishers.api.views.FisherChangeZoneAPIView.permission_classes", new=[])
    def test_fisher_change_zone_invalid_data_error(
        self, authenticated_user_with_coins, api_request_factory, api_view
    ):
        """
        GIVEN an authenticated user with coins
        WHEN the user attempts to change their zone with invalid data
        THEN the API returns a 400 Bad Request response due to invalid input"""
        payload = {"new_zone": "LAKE" * 50}

        request = api_request_factory.patch(path=API_PATH, data=payload, format="json")
        request.user = authenticated_user_with_coins

        response = api_view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("fishers.api.views.FisherChangeZoneAPIView.permission_classes", new=[])
    def test_fisher_change_zone_invalid_repository_error(
        self, authenticated_user_without_coins, api_request_factory, api_view
    ):
        """
        GIVEN an authenticated user without coins
        WHEN the user attempts to change their zone
        THEN the API returns a 500 Internal Server Error response due to insufficient coins
        """

        payload = {"new_zone": "LAKE"}

        request = api_request_factory.patch(path=API_PATH, data=payload, format="json")
        request.user = authenticated_user_without_coins

        response = api_view(request)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
