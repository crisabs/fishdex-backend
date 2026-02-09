from typing import Any, Dict

from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from capture.infrastructure.repositories.capture_write_repository import (
    capture_fish_repository,
)
from capture.infrastructure.repositories.capture_read_repository import (
    get_item_effect,
)
import logging
import random

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
