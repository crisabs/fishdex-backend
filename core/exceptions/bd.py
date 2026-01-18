from .base import AppException
from rest_framework import status


class ErrorRegistrationAccountExist(AppException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "ACCOUNT_REGISTRATION_ERROR"
    default_message = "The current data already is registered with an account"
