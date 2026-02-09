from django.db import DatabaseError
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fish.models import Fish
from fishers.models import Fisher
from inventory.models import FisherFish


def capture_fish_repository(user, fish_id, fish_weight, fish_length):
    """
    Persist a captured fish for a given user.

    Retrieves the corresponding Fisher and Fish entities and creates a
    FisherFish record with the captured fish's weight and length.

    Raises;
        FisherNotFoundError: If no Fisher is accociated with the given user.
        FishersNotFoundInDatabase: If the specified Fish does not exist.
        RepositoryError: If a database error occurs during persistence.
    """
    try:
        fisher = Fisher.objects.get(user=user)
        fish = Fish.objects.get(fish_id=fish_id)
        fisherFish = FisherFish.objects.create(
            fisher=fisher, fish=fish, weight=fish_weight, length=fish_length
        )
        fisherFish.save()

    except Fisher.DoesNotExist as exc:
        raise FisherNotFoundError from exc
    except Fish.DoesNotExist as exc:
        raise FishesNotFoundInDatabase from exc
    except DatabaseError as exc:
        raise RepositoryError from exc
