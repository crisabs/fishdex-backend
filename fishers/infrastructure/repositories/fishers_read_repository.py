from fishers.models import Fisher
from django.db import DatabaseError
import logging
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError

logger = logging.getLogger(__name__)


def get_fisher_details_me_repository(user):
    try:
        fisher = Fisher.objects.get(user=user)
        return {
            "nickname": fisher.nickname,
            "level": fisher.level,
            "coins": fisher.coins,
            "current_zone": fisher.current_zone,
        }
    except Fisher.DoesNotExist:
        raise FisherNotFoundError
    except DatabaseError as e:
        logger.exception("Database error while fetching fisher")
        raise RepositoryError from e
