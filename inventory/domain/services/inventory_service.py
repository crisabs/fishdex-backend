from typing import Any, Dict
from inventory.infrastructure.repositories.inventory_read_repository import (
    get_inventory_item_list_repository,
)
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotEnoughCoinsError, FisherNotFoundError

import logging

logger = logging.getLogger(__name__)


def get_inventory_item_list(user) -> list[Dict[str, Any]]:
    """
    Retrieve inventory item list for the given user.

    Args:
        user: An authenticated user instance.

    Returns: A dictionary containing the inventory items associated with the user.

    Raises:
        FisherNotFoundError: If the user has not associated fisher profile.
        RepositoryError: If a database access error occurs.
    """
    try:
        return get_inventory_item_list_repository(user=user)
    except FisherNotFoundError:
        logger.exception(
            "No fisher profile associated with user while retrieving inventory items"
        )
        raise
    except FisherNotEnoughCoinsError:
        logger.exception("Fisher has not enough coins for the purchase")
        raise
    except RepositoryError:
        logger.exception(
            "Repository failure while retrieving inventory item list for user"
        )
        raise
