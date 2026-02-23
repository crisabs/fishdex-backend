from unittest.mock import patch

import pytest
from core.exceptions.bd import RepositoryError
from core.exceptions.domain import FisherNotFoundError
from inventory.domain.services.inventory_service import (
    set_description_fisher_fish,
)


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser", password="testpassword"
    )


@pytest.mark.django_db
@patch(
    "inventory.domain.services.inventory_service.set_description_fisher_fish_repository"
)
class TestInventoryFisherFishDescriptionServiceSuccess:

    def test_set_description_fisher_fish_success_returns_data(self, mocker, user):
        mocker.return_value = {"success": True}

        response = set_description_fisher_fish(
            user=user,
            pk=1,
            description="New description",
        )
        assert response == {"success": True}


@pytest.mark.django_db
class TestInventoryFisherFishDescriptionServiceErrorHandling:

    @patch(
        "inventory.domain.services.inventory_service.set_description_fisher_fish_repository"
    )
    def test_set_description_fisher_fish_repository_raises_fisher_not_found_error(
        self, mocker, user
    ):
        mocker.side_effect = FisherNotFoundError("Fisher not found")

        with pytest.raises(FisherNotFoundError) as exc_info:
            set_description_fisher_fish(
                user=user,
                pk=1,
                description="New description",
            )
        assert str(exc_info.value) == "Fisher not found"

    @patch(
        "inventory.domain.services.inventory_service.set_description_fisher_fish_repository"
    )
    def test_set_description_fisher_fish_repository_raises_repository_error(
        self, mocker, user
    ):
        mocker.side_effect = RepositoryError("Database error")

        with pytest.raises(RepositoryError) as exc_info:
            set_description_fisher_fish(
                user=user,
                pk=1,
                description="New description",
            )
        assert str(exc_info.value) == "Database error"
