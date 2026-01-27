from typing import Dict, Any
from fish.models import Fish
from django.db import DatabaseError
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError


def get_fish_list_repository() -> list[Dict[str, Any]]:
    try:
        return list(Fish.objects.values())
    except Fish.DoesNotExist as exc:
        raise FishesNotFoundInDatabase from exc
    except DatabaseError as exc:
        raise RepositoryError from exc
