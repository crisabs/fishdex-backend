from fishers.models import Fisher
from django.db import DatabaseError
import logging
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError

logger = logging.getLogger(__name__)


def get_fisher_details_me_repository(user):
    """
    GIVEN a user that may or may have a corresponding Fisher record
    WHEN the repository function is called to fetch the fisher's details
    THEN it returns the fisher's nickname, level, couns, and current zone if the record exists,
    or raises FisherNotFoundError if not found,
    or RepositoryError if a database error occurs
    """
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


def get_fisher_coins(user):
    """
    GIVEN a user that may or may not have a corresponding Fisher record
    WHEN the repository function is called to fetch the user's coin balance
    THEN it returns the number of coins if the fisher exists,
    or raises FisherNotFoundError if not found,
    or RepositoryError if database error occurs
    """
    try:
        fisher = Fisher.objects.get(user=user)
        return fisher.coins
    except Fisher.DoesNotExist:
        raise FisherNotFoundError
    except DatabaseError as e:
        logger.exception("Database error while fetching fisher")
        raise RepositoryError from e
