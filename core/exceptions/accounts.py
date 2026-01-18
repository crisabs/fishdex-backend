from .base import AppException
from rest_framework import status


class ErrorAccountRegister(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "ERROR_ACCOUNT_CREATION"
    default_message = "Invalid data for the account creation"
