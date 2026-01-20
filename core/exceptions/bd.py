from .base import AppException


class RepositoryError(AppException):
    default_code = "REPOSITORY_ERROR"
    default_message = "An unexpected database error ocurred."


class AccountAlreadyExistsError(AppException):
    default_code = "ACCOUNT_ALREADY_EXIST"
    default_message = "Account already exist"
