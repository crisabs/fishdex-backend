from decimal import Decimal
from typing import Any, Dict
from inventory.infrastructure.repositories.inventory_read_repository import (
    get_inventory_item_list_repository,
    get_inventory_fish_list_repository,
)
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from math import floor

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
    except RepositoryError:
        logger.exception(
            "Repository failure while retrieving inventory item list for user"
        )
        raise


def get_inventory_fish_list(user) -> list[Dict[str, Any]]:
    """
    Retrieve inventory fish list for the given user.

    Args:
        user: An authenticated user instance.

    Returns: A dictionary containing the inventory fishes associated with the user.

    Raises:
        FisherNotFoundError: If the user has not associated fisher profile.
        RepositoryError: If a database access error occurs.
    """
    try:
        fishes_list = get_inventory_fish_list_repository(user=user)
        inventory = []

        for fish in fishes_list:
            price = floor(Decimal(fish["fish__base_price"]) * (fish["weight"]))

            inventory.append(
                {
                    "fish_name": fish["fish__name"],
                    "price": price,
                    "weight": fish["weight"],
                    "caught_at": fish["caught_at"],
                    "rarity": fish["fish__rarity"],
                }
            )
        return inventory

    except FisherNotFoundError:
        logger.exception(
            "No fisher profile associated with user while retrieving inventory fishes"
        )
        raise
    except RepositoryError:
        logger.exception(
            "Repository failure while retrieving inventory fish list for user"
        )
        raise
