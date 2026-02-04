from .base import AppException
from rest_framework import status


class AccountRegistrationError(AppException):
    default_code = "ACCOUNT_REGISTRATION_ERROR"
    default_detail = "Account registration failed"


class UserNotFoundError(AppException):
    default_code = "USER_NOT_FOUND"
    default_detail = "User not found"


class FisherNotFoundError(AppException):
    default_code = "FISHER_NOT_FOUND"
    default_detail = "The authenticated user has no fisher profile."


class ItemStoreNotFoundError(AppException):
    default_code = "ITEM_NOT_FOUND"
    default_detail = "Item not found"


class FisherNotEnoughCoinsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "NOT_ENOUGH_COINS"
    default_detail = "Not enough coins error for the current purchase"
