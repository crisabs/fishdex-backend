from store.infrastructure.store_write_repository import buy_item_repository


def buy_item(user, item_code, quantity) -> str:
    """
    Application service to purchase a store item for a user.

    Delegates the operation to the repository layer, handling
    validation, inventory update, and coin decution.

    Parameters
    user : User
        Authenticated user making the purchase.
    item_code : str
        Store item identifier.
    quantit : int
        Number of items to buy.

    Returns
    str
        Confirmation message from the repository
    """
    return buy_item_repository(user=user, item_code=item_code, quantity=quantity)
