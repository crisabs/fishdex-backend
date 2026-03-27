from decimal import Decimal
from math import floor


import logging

logger = logging.getLogger(__name__)


def get_fisher_fish_price(fisher_fish_base_price, fisher_fish_weight):

    price = floor(Decimal(fisher_fish_base_price) * Decimal(fisher_fish_weight))
    logger.debug(
        f"fisher fish base price {fisher_fish_base_price} fisher fish weight {fisher_fish_weight}"
    )

    return price
