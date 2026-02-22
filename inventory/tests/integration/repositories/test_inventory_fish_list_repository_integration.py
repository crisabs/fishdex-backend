from decimal import Decimal
from fish.models import Fish
from fishers.models import Fisher
from inventory.models import FisherFish
import pytest
from inventory.domain.services.inventory_service import (
    get_inventory_fish_list_repository,
)
from django.utils import timezone


@pytest.fixture
def user_with_fisher(django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )
    fisher = Fisher.objects.create(user=user, nickname=user)
    return user, fisher


@pytest.fixture
def user_without_fisher(django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )


@pytest.mark.integration
@pytest.mark.django_db
def test_inventory_fish_list_repository_success_integration(user_with_fisher):
    """
    GIVEN a user with an associated Fisher profile
    and at least one caught fish in the inventory
    WHEN the repository retreives the inventory fishes for that user
    THEN it should return a list containing the fish details with correct fields
    """

    user, fisher = user_with_fisher

    fish, _ = Fish.objects.get_or_create(name="Salmon", fish_id=1)

    FisherFish.objects.get_or_create(
        fisher=fisher, fish=fish, weight=Decimal("1"), length=Decimal("1")
    )

    result = get_inventory_fish_list_repository(user=user)

    assert result[0]["fish__name"] == "Salmon"
    assert result[0]["pk"] == 1
    assert result[0]["fish__base_price"] == 15
    assert result[0]["fish__rarity"] == "COMMON"
    assert result[0]["weight"] == Decimal("1.00")

    assert isinstance(result[0]["caught_at"], timezone.datetime)
