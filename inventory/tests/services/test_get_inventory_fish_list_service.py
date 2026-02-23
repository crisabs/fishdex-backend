from django.utils import timezone
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from fishers.models import Fisher
from inventory.domain.services.inventory_service import get_inventory_fish_list
from unittest.mock import patch
import pytest


@pytest.fixture
def user_with_fisher_profile(db, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )
    Fisher.objects.create(user=user, nickname=user)
    return user


@pytest.fixture
def user_without_fisher_profile(db, django_user_model):
    return django_user_model.objects.create_user(
        username="user_test@test.com", password="user_test"
    )


class TestGetInventoryFishListServiceSuccess:

    @patch(
        "inventory.domain.services.inventory_service.get_inventory_fish_list_repository"
    )
    def test_get_inventory_fish_list_service_returns_data(
        self, mock_repository, user_with_fisher_profile
    ):
        """
        GIVEN a user with a fisher profile
        AND a mocked repository returning a list of fishes
        WHEN get_inventory_fish_list is called
        THEN it should return the expected list of fishes with correct data
        """

        caught_at = timezone.now()
        mock_repository.return_value = [
            {
                "fish__name": "Salmon",
                "fish__base_price": 15,
                "pk": 1,
                "weight": 0.3,
                "caught_at": caught_at,
                "fish__rarity": "COMMON",
            },
        ]

        expected_result = [
            {
                "fish_name": "Salmon",
                "price": 4,
                "pk": 1,
                "weight": 0.3,
                "caught_at": caught_at,
                "rarity": "COMMON",
            }
        ]
        result = get_inventory_fish_list(user=user_with_fisher_profile)
        assert result == expected_result
        assert result[0]["caught_at"] is caught_at


class TestGetInventoryFishListServiceErrors:
    @patch(
        "inventory.domain.services.inventory_service.get_inventory_fish_list_repository"
    )
    def test_get_inventory_fish_list_service_raises_fisher_not_found_error(
        self, mock_repository, user_without_fisher_profile
    ):
        """
        GIVEN a user without a fisher profile
        AND a mocked repository raising FisherNotFoundError
        WHEN get_inventory_fish_list is called
        THEN it should raise FisherNotFoundError
        """

        mock_repository.side_effect = FisherNotFoundError()

        with pytest.raises(FisherNotFoundError):
            get_inventory_fish_list(user=user_without_fisher_profile)

    @patch(
        "inventory.domain.services.inventory_service.get_inventory_fish_list_repository"
    )
    def test_get_inventory_fish_list_service_raises_repository_error(
        self, mock_repository, user_with_fisher_profile
    ):
        """
        GIVEN a user with a fisher profile
        AND a mocked repository raising RepositoryError
        WHEN get_inventory_fish_list is called
        THEN it should raise RepositoryError
        """

        mock_repository.side_effect = RepositoryError()

        with pytest.raises(RepositoryError):
            get_inventory_fish_list(user=user_with_fisher_profile)
