from typing import Dict, Any, cast

from rest_framework.exceptions import ValidationError
from accounts.infrastructure.repositories.accounts_write_repository import (
    create_account_repository,
)
import logging
from core.exceptions.bd import AccountAlreadyExistsError, RepositoryError
from rest_framework_simplejwt.tokens import RefreshToken, Token


logger = logging.getLogger(__name__)


def register_account(email, password) -> Dict[str, Any]:
    """
    Creates a new  account using the provided email and password

    Raises:
      AccountAlreadyExistsError: if an account with the given email aleady exists
      or if a repository error occurs during account creation.
    """
    try:
        create_account_repository(email=email, password=password)
        return {"data": "OK"}
    except AccountAlreadyExistsError:
        raise
    except RepositoryError as e:
        logger.exception("Repository error during account registration")
        raise AccountAlreadyExistsError from e


def logout_account(refresh_token: str) -> None:
    """
    Invalidates a refresh token by adding it to the blacklist.
    Raises ValidationError if the token is missing or invalid.
    """
    if not refresh_token:
        raise ValidationError("refresh token required")
    try:
        token = RefreshToken(cast(Token, refresh_token))
        token.blacklist()
    except Exception:
        raise ValidationError("invalid or expired refresh token")
