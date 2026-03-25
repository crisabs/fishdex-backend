from core.exceptions.bd import RepositoryError
from store.infrastructure.store_write_repository import buy_item_repository
from store.infrastructure.store_read_repository import (
    get_rod_store_list_repository,
    get_bait_store_list_repository,
)


def buy_item(user, item_code, quantity) -> str:
    """
    Application service to purchase a store item for a user.

    Delegates the operation to the repository layer, handling
    validation, inventory update, and coin deduction.

    Parameters
    user : User
        Authenticated user making the purchase.
    item_code : str
        Store item identifier.
    quantity : int
        Number of items to buy.

    Returns
    str
        Confirmation message from the repository
    """
    return buy_item_repository(user=user, item_code=item_code, quantity=quantity)


def get_rod_store_list():
    try:
        return get_rod_store_list_repository()
    except RepositoryError:
        raise


def get_bait_store_list():
    try:
        return get_bait_store_list_repository()
    except RepositoryError:
        raise
