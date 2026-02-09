from .base import AppException


class RepositoryError(AppException):
    default_code = "REPOSITORY_ERROR"
    default_detail = "An unexpected database error ocurred."


class AccountAlreadyExistsError(AppException):
    default_code = "ACCOUNT_ALREADY_EXIST"
    default_detail = "Account already exist"


class FishesNotFoundInDatabase(AppException):
    default_code = "NOT_FOUND_FISHES_IN_REPOSITORY"
    default_detail = "Not fishes were found in the database"


class FishNotFoundInDatabase(AppException):
    default_code = "NOT_FOUND_FISH_IN_REPOSITORY"
    default_detail = "Fish were not found in the database"
