from decimal import Decimal
from typing import Any, Dict
from inventory.infrastructure.repositories.inventory_read_repository import (
    get_inventory_item_list_repository,
    get_inventory_fish_list_repository,
    get_price_fish_to_sell,
)
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from math import floor
from inventory.infrastructure.repositories.inventory_write_repository import (
    sell_fish_repository,
)
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

        for fisherFish in fishes_list:
            price = floor(
                Decimal(fisherFish["fish__base_price"]) * Decimal(fisherFish["weight"])
            )

            inventory.append(
                {
                    "fish_name": fisherFish["fish__name"],
                    "price": price,
                    "weight": fisherFish["weight"],
                    "caught_at": fisherFish["caught_at"],
                    "rarity": fisherFish["fish__rarity"],
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


def sell_fish(user, pk, fish_id, total_weight):
    """
    Process the sale of a fish from a user's inventory.

    Calculates the total price of the fish based on its ID and weight,
    and delegates the sale operation to the repository layer.

    Args:
        user (User): The authenticated user performing the sale.
        pk (int): The primary key of the inventory record.
        fish_id (int): Identifier of the fish to sell.
        total_weight (float): Amount of fish weight to sell.

    Returns:
        dict: A dictionary containing the result of the operation.
              Example: {"code": "OK"}

    Raises:
        FisherNotFoundError: If the fisher associated with the user does not exist.
        RepositoryError: If there is a failure accessing or updating repository data.
    """

    total_price = get_price_fish_to_sell(fish_id=fish_id, total_weight=total_weight)
    """
    Persist the sale of a fish inventory record and update the fisher's balance.

    Retrieves the fisher associated with the given user and the corresponding
    inventory record, removes the inventory entry, and increments the fisher's
    coin balance by the provided total price. All operations are executed within
    a database transaction to ensure consistency.

    Args:
        user (User): The user associated with the fisher.
        pk (int): Primary key of the fisher fish inventory record.
        total_price (Decimal | float): Total price obtained from selling the fish.

    Returns:
        dict: A dictionary indicating a successful operation.
              Example: {"code": "OK"}

    Raises:
        FisherNotFoundError: If no fisher exists for the given user.
        FisherFishNotFoundError: If the inventory record does not exist.
        RepositoryError: If a database-level error occurs during the operation.
    """
    try:
        result = sell_fish_repository(
            user=user,
            pk=pk,
            total_price=total_price,
        )
        return result

    except FisherNotFoundError:
        logger.exception("Repository failure while retrieving fisher data")
        raise
    except RepositoryError:
        logger.exception("Repository failure while retrieving fisher fish data")
        raise
