from typing import Any, Dict
from fish.infrastructure.repositories.fish_read_repository import (
    get_fish_list_repository,
    get_fish_details_repository,
)
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError
import logging

logger = logging.getLogger(__name__)


def get_fish_list() -> list[Dict[str, Any]]:
    """
    Retrieves the complete fish list via the service layer

    :return: A list of all fishes available to capture in all the zones
    :rtype: list[Dict[str, Any]]
    """
    try:
        return get_fish_list_repository()
    except RepositoryError:
        logger.exception("Database error while retrieving fish list")
        raise


def get_fish_details(fish_id: int) -> Dict[str, Any]:
    """
    Retrieve the details of a fish by its fish_id.

    Args:
        fish_id: Identifies of the fish to retrieve.

    Returns:
        A dictionary containing the fish details.

    Raises:
       FishesNotFoundInDatabase: if the fish does not exist.
       RepositoryError: If a database access error occurs.
    """
    try:
        return get_fish_details_repository(fish_id=fish_id)
    except FishesNotFoundInDatabase:
        logger.warning(
            "Fish not found when retrieving fish details", extra={"fish_id": fish_id}
        )
        raise
    except RepositoryError:
        logger.exception(
            "Database error while retrieving fish details", extra={"fish_id": fish_id}
        )
        raise
