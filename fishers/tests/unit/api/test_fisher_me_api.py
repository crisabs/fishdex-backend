import pytest
from pytest import fixture
from unittest.mock import MagicMock, patch
from rest_framework import status
from rest_framework.test import APIRequestFactory
from core.exceptions.domain import FisherNotFoundError
from fishers.api.views import FisherMeAPIView
from django.contrib.auth.models import AbstractBaseUser


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.fixture
def api_view():
    return FisherMeAPIView.as_view()


@fixture
def authenticated_user() -> AbstractBaseUser:
    fake_user = MagicMock()
    fake_user.is_authenticated = True
    return fake_user


@fixture
def unauthenticated_user() -> AbstractBaseUser:
    return MagicMock()


class TestFisherMeSuccess:
    @patch("fishers.api.views.FisherMeAPIView.permission_classes", new=[])
    @patch("fishers.api.views.get_fisher_detail_me")
    def test_fisher_me_authenticated_user_returns_fisher_data(
        self, mock_get_fisher_detail_me, authenticated_user, api_factory, api_view
    ):
        """
        GIVEN an authenticated user
        WHEN requesting fisher details
        THEN returns status 200 and fisher data
        """

        mock_get_fisher_detail_me.return_value = {
            "nickname": "Old Fisher",
            "level": 33,
            "coins": 35,
            "current_zone": "River",
        }

        request = api_factory.get(path="/fishers/me/")
        request.user = authenticated_user

        response = api_view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["result"]["nickname"] == "Old Fisher"

        mock_get_fisher_detail_me.assert_called_once_with(user=request.user)


class TestFisherMeErrors:
    def test_fisher_me_user_not_authenticated(
        self, api_factory, api_view, unauthenticated_user
    ):
        """
        GIVEN an unauthenticated request
        WHEN accessing the endpoint
        THEN returns 401 Unauthorized
        """

        request = api_factory.get(path="/fishers/me/")
        request.user = unauthenticated_user

        response = api_view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "credentials" in response.data["detail"].lower()

    @patch("fishers.api.views.FisherMeAPIView.permission_classes", new=[])
    @patch("fishers.api.views.get_fisher_detail_me")
    def test_fisher_me_fisher_not_found_error(
        self, mock_service, api_factory, api_view, authenticated_user
    ):
        """
        GIVEN an authenticated user without a fisher profile
        WHEN requesting fisher details
        THEN returns status 404 Not Found with appropriate error message
        """

        mock_service.side_effect = FisherNotFoundError()

        request = api_factory.get(path="/fishers/me/")
        request.user = authenticated_user

        response = api_view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        mock_service.assert_called_once_with(user=request.user)
