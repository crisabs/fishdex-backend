from typing import Any, Dict

from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from capture.infrastructure.repositories.capture_write_repository import (
    capture_fish_repository,
)
from capture.infrastructure.repositories.capture_read_repository import (
    get_item_effect,
    get_list_fishes_by_habitat_repository,
    get_fisher_zone_repository,
)
import logging
import random

from fishers.tests.unit.services.test_fishers_service import user

logger = logging.getLogger(__name__)


def capture_fish_service(
    user, rod_code, bait_code, fish_id, fish_weight, fish_length
) -> Dict[str, Any]:
    try:
        """
        Executes the fish capture attempt for a user.

        Calculates the capture probability based on the rod and bait effects
        versus the fish weight, performs a randomized capture roll, and
        persists the capture if successful.

        Returns:
            Dict[str, Any]: A result indicating whether the fish was captured
            and a human-readable message.

        Raises:
            FisherNotFoundError: If the user has no associated Fisher.
            RepositoryError: If a persistence error occurs.
        """
        rod_effect = get_item_effect(item_code=rod_code)
        bait_effect = get_item_effect(item_code=bait_code)

        capture_power = rod_effect + bait_effect
        capture_probability = capture_power / (fish_weight + capture_power)

        random_roll = random.random()
        is_captured = random_roll < capture_probability

        if not is_captured:
            return {"captured": False, "message": "The fish escaped"}
        capture_fish_repository(
            user=user, fish_id=fish_id, fish_weight=fish_weight, fish_length=fish_length
        )

        return {"captured": True, "message": "Fish captured!"}

    except FisherNotFoundError:
        raise
    except RepositoryError:
        raise


def get_spawned_fish(user=user):
    """
    Returns a randomly spawned fish for the given user bases
    on the fisher's current zone.

    Fish rarity is selected using weighted probabilities, priorizing the chosen rarity
    and falling bck to any available fish when necessary.

    Raises:
        FisherNotFoundError: If the user has no associated fisher profile.
        NoFishAvailableError: If no fish are available for the fisher's zone.
    """
    try:
        fisher_zone = get_fisher_zone_repository(user=user)

        RARITY_WEIGHTS = {
            "COMMON": 70,
            "RARE": 25,
            "LEGENDARY": 5,
        }

        selected_rarity = random.choices(
            population=list(RARITY_WEIGHTS.keys()),
            weights=list(RARITY_WEIGHTS.values()),
            k=1,
        )[0]

        fishes = get_list_fishes_by_habitat_repository(habitat=fisher_zone)

        fishes_by_rarity = {"COMMON": [], "RARE": [], "LEGENDARY": []}
        for fish in fishes:
            fishes_by_rarity[fish["rarity"]].append(fish)

        if fishes_by_rarity[selected_rarity]:
            return random.choice(fishes_by_rarity[selected_rarity])["fish_id"]

        return random.choice(fishes)["fish_id"]
    except FisherNotFoundError:
        raise
