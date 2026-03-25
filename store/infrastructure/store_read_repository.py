from store.models import ItemStore

import logging

logger = logging.getLogger(__name__)


def get_rod_store_list_repository():
    qr_item_store_rod = (
        ItemStore.objects.filter(type="ROD")
        .select_related("item")
        .values("name", "price")
    )
    list_item_store_rod = list(qr_item_store_rod)
    logger.debug(list_item_store_rod)

    return list_item_store_rod


def get_bait_store_list_repository():
    qr_item_store_bait = (
        ItemStore.objects.filter(type="BAIT")
        .select_related("item")
        .values("name", "price")
    )
    list_item_store_bait = list(qr_item_store_bait)
    logger.debug(list_item_store_bait)

    return list_item_store_bait
