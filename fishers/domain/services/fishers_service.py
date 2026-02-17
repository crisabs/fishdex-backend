from typing import Dict, Any
from fish.models import Habitat
from fishers.infrastructure.repositories.fishers_read_repository import (
    get_fisher_details_me_repository,
    get_fisher_coins,
)
from fishers.infrastructure.repositories.fishers_write_repository import (
    set_fisher_nickname_repository,
    set_fisher_zone_repository,
)
from core.exceptions.domain import (
    FisherNotFoundError,
    InvalidZoneError,
    NotEnoughCoinsError,
    ZoneAlreadySetError,
)

from core.exceptions.bd import RepositoryError
import logging

logger = logging.getLogger(__name__)


def get_fisher_detail_me(user) -> Dict[str, Any]:
    """
    Returns the fisher profile associated with the authenticated user.

    Raises:
        FisherNotFoundError: If the user has no fisher profile.
        RepositoryError: If a database error occurs.
    """
    try:
        return get_fisher_details_me_repository(user=user)

    except FisherNotFoundError:
        raise
    except RepositoryError:
        logger.exception("Repository error while retrieving fisher profile")
        raise


def set_fisher_nickname(user, nickname: str) -> str:
    """
    Update a fisher's nickname via the service layer

    Args:
        user: Django User instance.
        nickname: New nickname.

    Returns:
        Confirmation message:

    Raises:
        FisherNotFoundError: No fisher profile for the user.
        RepositoryError: Database error during update.

    """
    try:
        return set_fisher_nickname_repository(user=user, nickname=nickname)
    except FisherNotFoundError:
        raise
    except RepositoryError:
        logger.exception("Repository error while changing fisher nickname")
        raise


def set_fisher_zone(user, new_zone):
    """
    GIVEN a user with a certain number of coins and a current fishing zone
    WHEN the user attempts to change to a new zone
    THEN the function either updates the zone and deducts the cost, or raises
    a specific exception if the new zone is invalid,
    already set, or the user has insufficient coins.
    """
    ZONE_COST = {"RIVER": 100, "LAKE": 200, "OCEAN": 500}

    new_zone = new_zone.upper()

    if new_zone not in ZONE_COST:
        raise InvalidZoneError()

    try:
        current_zone = get_fisher_details_me_repository(user=user)[
            "current_zone"
        ].upper()

        if current_zone == new_zone:
            raise ZoneAlreadySetError()

        zone_cost = ZONE_COST[new_zone]
        fisher_coins = get_fisher_coins(user=user)

        if fisher_coins < zone_cost:
            raise NotEnoughCoinsError()

        set_fisher_zone_repository(user=user, new_zone=new_zone, zone_cost=zone_cost)
        return {"code": "ZONE_CHANGED", "new_zone": new_zone}

    except FisherNotFoundError:
        logger.exception(FisherNotFoundError.default_detail)
        raise

    except RepositoryError:
        logger.exception(RepositoryError.default_detail)
        raise
