from django.db import DatabaseError
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherFishNotFoundError, FisherNotFoundError
from fishers.models import Fisher
from inventory.models import FisherFish
from django.db import transaction


def sell_fish_repository(user, pk, total_price):
    try:
        fisher = Fisher.objects.get(user=user)
        fisherFish = FisherFish.objects.get(fisher=fisher, pk=pk)

        with transaction.atomic():
            fisherFish.delete()
            fisher.coins += total_price
            fisher.save()

            return {"code": "OK"}

    except Fisher.DoesNotExist as exc:
        raise FisherNotFoundError from exc
    except FisherFish.DoesNotExist as exc:
        raise FisherFishNotFoundError from exc
    except DatabaseError as exc:
        raise RepositoryError from exc
