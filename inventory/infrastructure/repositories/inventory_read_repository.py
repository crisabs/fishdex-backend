from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FishNotFoundError, FisherNotFoundError
from fishers.models import Fisher
from fish.models import Fish
from inventory.models import FisherFish, FisherItem
import logging

logger = logging.getLogger(__name__)


def get_inventory_item_list_repository(user):
    """
    Retrieve the inventory items for the given user.

    Returns a list of inventory entries containing items code, name and quantity.
    Requires the user to have an associated Fisher profile.
    """
    try:
        fisher = Fisher.objects.get(user=user)
        fisher_items = list(
            FisherItem.objects.filter(fisher=fisher)
            .select_related("item")
            .values("item__code", "item__name", "quantity")
        )

        inventory = [
            {
                "item_code": item["item__code"],
                "item_name": item["item__name"],
                "quantity": item["quantity"],
            }
            for item in fisher_items
        ]

        return inventory
    except Fisher.DoesNotExist:
        raise FisherNotFoundError
    except DatabaseError as exc:
        raise RepositoryError from exc


def get_inventory_fish_list_repository(user):
    """
    Retrieve the inventory fishes for the given user.

    Returns a list of inventory entries containing
    fish name, base_price, weight, caught_at and rarity.
    Requires the user to have an associated Fisher profile.
    """
    try:
        fisher = Fisher.objects.get(user=user)
        return list(
            FisherFish.objects.filter(fisher=fisher)
            .select_related("fish")
            .values(
                "fish__name",
                "fish__base_price",
                "weight",
                "pk",
                "caught_at",
                "fish__rarity",
            )
        )
    except Fisher.DoesNotExist:
        raise FisherNotFoundError
    except DatabaseError as exc:
        raise RepositoryError from exc


def get_price_fish_to_sell(fish_id, total_weight):
    """
    Calculate the sale price of a fish based on its weight.

    Retrieves the fish by its identifier and computes the total price
    using its base price and the provided weight.

    Args:
        fish_id (int): Identifier of the fish.
        total_weight (float): Weight of the fish to sell.

    Returns:
        Decimal | float: Total sale price.

    Raises:
        FishNotFoundError: If the fish does not exist.
    """

    try:
        fish = Fish.objects.get(fish_id=fish_id)
        return fish.base_price * total_weight
    except Fish.DoesNotExist as exc:
        raise FishNotFoundError from exc
