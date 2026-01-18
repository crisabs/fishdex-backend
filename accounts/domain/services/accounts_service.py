from typing import Dict, Any
from accounts.infrastructure.repositories.accounts_write_repository import (
    create_account_repository,
)
import logging
from core.exceptions.bd import AccountAlreadyExistsError, RepositoryError

logger = logging.getLogger(__name__)


def register_account(email, password) -> Dict[str, Any]:
    try:
        create_account_repository(email=email, password=password)
        return {"data": "OK"}
    except AccountAlreadyExistsError:
        raise
    except RepositoryError as e:
        logger.exception("Repository error during account registration")
        raise AccountAlreadyExistsError from e
