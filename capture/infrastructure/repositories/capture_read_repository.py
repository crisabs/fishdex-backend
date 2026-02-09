from django.db import DatabaseError
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError
from store.models import ItemStore


def get_item_effect(item_code):
    """
    Revieves the effect value of a store item by its code.

    Looks up the item in the store and returns its effect attribute.

    Raises:
        FishesNotFoundInDatabase: If tht item with the given code does not exist.
        RepositoryError: If a database error occurs during retrieval.
    """
    try:
        item = ItemStore.objects.get(code=item_code)
        return item.effect
    except ItemStore.DoesNotExist as exc:
        raise FishesNotFoundInDatabase from exc
    except DatabaseError as exc:
        raise RepositoryError from exc
