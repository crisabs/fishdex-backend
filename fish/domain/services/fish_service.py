from typing import Any, Dict
from fish.infrastructure.repositories.fish_read_repository import (
    get_fish_list_repository,
)
from core.exceptions.bd import RepositoryError


def get_fish_list() -> list[Dict[str, Any]]:
    """
    Retrieves the complete fish list via the service layer

    :return: A list of all fishes available to capture in all the zones
    :rtype: list[Dict[str, Any]]
    """
    try:
        return get_fish_list_repository()
    except RepositoryError:
        raise
