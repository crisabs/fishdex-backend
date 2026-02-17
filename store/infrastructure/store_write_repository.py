from fishers.models import Fisher
from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import (
    NotEnoughCoinsError,
    FisherNotFoundError,
    ItemStoreNotFoundError,
)
from django.db import transaction
from inventory.models import FisherItem
from store.models import ItemStore


def buy_item_repository(user, item_code, quantity):
    """
    Purchase a store item for a fisher.

    Validates fisher and item existence, checks coins, updates inventory,
    and decuts coins atomically.

    Parameters
    user: User
        Authenticated user making the purchase.
    item_code: str
        Store item identifier.
    quantity : int
        Number of items to buy.

    Returns
    str
        Confirmation message with item, quantity, and total cost.

    Raises
    FisherNotFoundError
    ItemStoreNotFoundError
    FisherNotEnoughCoinsError
    RepositoryError
    """

    try:
        fisher = Fisher.objects.get(user=user)
        item = ItemStore.objects.get(code=item_code)

        total_price = item.price * quantity
        if total_price > fisher.coins:
            raise NotEnoughCoinsError()

        with transaction.atomic():
            fisherItem, created = FisherItem.objects.update_or_create(
                fisher=fisher,
                item=item,
            )
            if not created:
                fisherItem.quantity += quantity
                fisherItem.save(update_fields=["quantity"])

            fisher.coins -= total_price
            fisher.save(update_fields=["coins"])

            return f"OK: {item.name} ({item.price})x{quantity} = {total_price} coins"

    except Fisher.DoesNotExist as exc:
        raise FisherNotFoundError from exc
    except ItemStore.DoesNotExist as exc:
        raise ItemStoreNotFoundError from exc
    except DatabaseError as exc:
        raise RepositoryError from exc
