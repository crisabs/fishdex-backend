from typing import Dict, Any
from fishers.infrastructure.repositories.fishers_read_repository import (
    get_fisher_details_me_repository,
)
from fishers.infrastructure.repositories.fishers_write_repository import (
    set_fisher_nickname_repository,
)
from core.exceptions.domain import FisherNotFoundError

from core.exceptions.bd import RepositoryError
import logging

logger = logging.getLogger(__name__)


def get_fisher_detail_me(user) -> Dict[str, Any]:
    """
    Returns the fisher profile associated with the authenticated user.

    Raises:
        FisherNotFoundError: If the user has no fisher profile.
        RepositoryError: If a database error occurs.
    """
    try:
        return get_fisher_details_me_repository(user=user)

    except FisherNotFoundError:
        raise
    except RepositoryError:
        logger.exception("Repository error while retrieving fisher profile")
        raise


def set_fisher_nickname(user, nickname: str) -> str:
    """
    Update a fisher's nickname via the service layer

    Args:
        user: Django User instance.
        nickname: New nickname.

    Returns:
        Confirmation message:

    Raises:
        FisherNotFoundError: No fisher profile for the user.
        RepositoryError: Database error during update.

    """
    try:
        return set_fisher_nickname_repository(user=user, nickname=nickname)
    except FisherNotFoundError:
        raise
    except RepositoryError:
        logger.exception("Repository error while changing fisher nickname")
        raise
