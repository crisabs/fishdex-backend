from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher
from inventory.models import FisherItem

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
