from django.db import DatabaseError
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError
from core.exceptions.domain import FisherNotFoundError, ItemStoreNotFoundError
from fish.models import Fish
from fishers.models import Fisher
from inventory.models import FisherFish, FisherItem
from store.models import ItemStore
from django.db import transaction
from django.db.models import F


def capture_fish_repository(user, fish_id, fish_weight, fish_length):
    """
    Persist a captured fish for a given user.

    Retrieves the corresponding Fisher and Fish entities and creates a
    FisherFish record with the captured fish's weight and length.

    Raises;
        FisherNotFoundError: If no Fisher is associated with the given user.
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


def update_bait_quantity_repository(user, bait_code):
    try:
        with transaction.atomic():
            fisher = Fisher.objects.get(user=user)
            item = ItemStore.objects.get(code=bait_code)

            fisherItem = FisherItem.objects.get(fisher=fisher, item=item)

            if fisherItem.quantity <= 0:
                raise ValueError("No enough quantity")

            fisherItem.quantity = F("quantity") - 1
            fisherItem.save()

            fisherItem.refresh_from_db()

    except Fisher.DoesNotExist as exc:
        raise FisherNotFoundError from exc
    except ItemStore.DoesNotExist as exc:
        raise ItemStoreNotFoundError from exc
    except DatabaseError as exc:
        raise RepositoryError from exc


def update_rod_quantity_repository(user, rod_code):
    try:
        with transaction.atomic():
            fisher = Fisher.objects.get(user=user)
            item = ItemStore.objects.get(code=rod_code)

            fisherItem = FisherItem.objects.get(fisher=fisher, item=item)
            if fisherItem.quantity <= 0:
                raise ValueError("no enough quantity")

            fisherItem.quantity = F("quantity") - 1
            fisherItem.save()

            fisherItem.refresh_from_db()

    except Fisher.DoesNotExist as exc:
        raise FisherNotFoundError from exc
    except ItemStore.DoesNotExist as exc:
        raise ItemStoreNotFoundError from exc
    except DatabaseError as exc:
        raise RepositoryError from exc
