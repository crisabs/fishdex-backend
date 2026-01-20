from .base import AppException


class AccountRegistrationError(AppException):
    default_code = "ACCOUNT_REGISTRATION_ERROR"
    default_message = "Account registration failed"


class UserNotFoundError(AppException):
    default_code = "USER_NOT_FOUND"
    default_message = "User not found"


class FisherNotFoundError(AppException):
    default_code = "FISHER_NOT_FOUND"
    default_message = "The authenticated user has no fisher profile."
