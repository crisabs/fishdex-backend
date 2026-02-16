from django.db import DatabaseError
from core.exceptions.bd import FishesNotFoundInDatabase, RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fish.models import Fish, Habitat
from store.models import ItemStore
from fishers.models import Fisher
import logging

logger = logging.getLogger(__name__)


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


def get_list_fishes_by_habitat_repository(habitat):
    try:
        fishes = Fish.objects.filter(habitat=habitat)
        logger.info("fishes  %s", fishes)
        fishes_list = [
            {
                "fish_id": fish.fish_id,
                "rarity": fish.rarity,
            }
            for fish in fishes
        ]
        return fishes_list
    except Fisher.DoesNotExist as exc:
        raise FisherNotFoundError from exc


def get_fisher_zone_repository(user):
    try:
        fisher = Fisher.objects.get(user=user)
        return Habitat[fisher.current_zone.upper()].value
    except Fisher.DoesNotExist as exc:
        raise FisherNotFoundError from exc
