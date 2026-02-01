from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher

# TODO replace the dummy implementation
_dummy_data = {
    "store_items": [
        {"name": "Basic Rod", "type": "ROD", "effect": 0.3, "price": 100},
        {"name": "Basic Bait", "type": "BAIT", "effect": 0.3, "price": 100},
        {"name": "Super Bait", "type": "BAIT", "effect": 0.3, "price": 400},
    ],
    "fishes": [
        {
            "name": "Salmon",
            "fish_id": 1,
            "description": "A strong migratory fish known for swimming upstream.",
            "habitat": "RIVER",
            "rarity": "COMMON",
            "base_weight": 3.0,
            "base_price": 15.0,
        },
    ],
}


def get_inventory_item_list_repository(user):
    try:
        return _dummy_data
    except Fisher.DoesNotExist:
        raise FisherNotFoundError
    except DatabaseError as exc:
        raise RepositoryError from exc
