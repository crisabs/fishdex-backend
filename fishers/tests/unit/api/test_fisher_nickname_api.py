from pytest import fixture
from unittest.mock import MagicMock, patch
from rest_framework import status
from core.exceptions.bd import RepositoryError
from rest_framework.test import APIRequestFactory
from fishers.api.views import FisherNicknameAPIView

API_PATH = "/fishers/nickname/"


@fixture
def api_factory():
    return APIRequestFactory()


@fixture
def api_view():
    return FisherNicknameAPIView.as_view()


@fixture
def authenticated_user():
    fake_user = MagicMock()
    fake_user.is_authenticated = True
    return fake_user


@fixture
def unauthenticated_user():
    fake_user = MagicMock()
    fake_user.is_authenticated = False
    return fake_user


class TestFisherNicknameSuccess:

    @patch("fishers.api.views.FisherNicknameAPIView.permission_classes", new=[])
    @patch("fishers.api.views.set_fisher_nickname")
    def test_fisher_nickname_success(
        self, mock_service, authenticated_user, api_factory, api_view
    ):
        """
        GIVEN an authenticated user
        WHEN the nickname update endpoint is called
        THEN it returns a confirmation message with HTTP 200
        """

        payload = {"nickname": "OldFisher"}
        mock_service.return_value = f"Fisher nickname updated to {payload['nickname']}"

        request = api_factory.patch(path=API_PATH, data=payload, format="json")
        request.user = authenticated_user

        response = api_view(request)

        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"Fisher nickname updated to {payload['nickname']}"
        )

        mock_service.assert_called_once_with(
            user=request.user, nickname=payload["nickname"]
        )


class TestFisherNicknameErrors:

    @patch("fishers.api.views.FisherNicknameAPIView.permission_classes", new=[])
    def test_fisher_nickname_invalid_payload(
        self, authenticated_user, api_factory, api_view
    ):
        """
        GIVEN an authenticated user
        WHEN payload is invalid
        THEN the API returns HTTP 400
        """
        payload = {"nickname": ""}
        request = api_factory.patch(path=API_PATH, data=payload, format="json")
        request.user = authenticated_user

        response = api_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("fishers.api.views.FisherNicknameAPIView.permission_classes", new=[])
    @patch("fishers.api.views.set_fisher_nickname")
    def test_fisher_nickname_internal_server_error(
        self, mock_service, api_factory, api_view, authenticated_user
    ):
        """
        GIVEN an authenticated user
        WHEN the nickname update service raises a repository error
        THEN the API returns HTTP 500
        """

        payload = {"nickname": "nickname"}

        request = api_factory.patch(path=API_PATH, data=payload, format="json")
        request.user = authenticated_user

        mock_service.side_effect = RepositoryError

        response = api_view(request)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_fisher_nickname_unauthenticated_user(
        self, unauthenticated_user, api_factory, api_view
    ):
        """
        GIVEN an user without authentication
        WHEN calling the nickname update endpoint
        THEN returns HTTP 401 Unauthorized
        """
        payload = {"nickname": "nickname"}

        request = api_factory.patch(path=API_PATH, data=payload, format="json")
        request.user = unauthenticated_user
        response = api_view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
