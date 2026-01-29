from typing import Dict, Any
from fish.models import Fish
from django.db import DatabaseError
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError


def get_fish_list_repository() -> list[Dict[str, Any]]:
    """
    Retrieve all fishes from the database.

    Returns:
        A list of dictionaries, each containing the fields of a Fish.

    Raises:
        FishesNotFoundInDatabase: If no fishes are found in the database.
        RepositoryError: If a database access error occurs.
    """
    try:
        return list(Fish.objects.values())
    except Fish.DoesNotExist as exc:
        raise FishesNotFoundInDatabase from exc
    except DatabaseError as exc:
        raise RepositoryError from exc


def get_fish_details_repository(fish_id: int) -> Dict[str, Any]:
    """
    Retrieve the details of a single fish by its fish_id from the database.

    Args:
        fish_id: Identifier of the fish to retrieve.

    Returns:
        A dictionary containing the fields of the fish.

    Raises:
        FishesNotFoundInDatabase: If the fish with the given fish_id does not exist.
        RepositoryError: If a database access error occurs.
    """
    try:
        fish = Fish.objects.get(fish_id=fish_id)
        return {
            "fish_id": fish.fish_id,
            "name": fish.name,
            "description": fish.description,
            "habitat": fish.habitat,
            "rarity": fish.rarity,
            "base_weight": fish.base_weight,
            "base_price": fish.base_price,
        }
    except Fish.DoesNotExist as exc:
        raise FishesNotFoundInDatabase from exc
    except DatabaseError as exc:
        raise RepositoryError from exc
