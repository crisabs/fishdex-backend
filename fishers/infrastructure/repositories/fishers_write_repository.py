from django.db import DatabaseError
from fishers.models import Fisher
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from django.db import transaction


def set_fisher_nickname_repository(user, nickname) -> str:
    """
    Update a fisher's nickname in the database atomically.

    Args:
        user: Django User instance.
        nickname: New nickname.

    Returns:
        Confirmation message.

    Raises:
        FisherNotFoundError: User has no fisher profile.
        RepositoryError: Databse error during update.
    """
    try:
        with transaction.atomic():
            fisher = Fisher.objects.get(user=user)
            fisher.nickname = nickname
            fisher.save()
            return f"Fisher nickname updated to {nickname}"
    except Fisher.DoesNotExist:
        raise FisherNotFoundError
    except DatabaseError as exc:
        raise RepositoryError from exc
