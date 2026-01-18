from .base import AppException


class AccountRegistrationError(AppException):
    default_code = "ACCOUNT_REGISTRATION_ERROR"
    default_message = "Account registration failed"
