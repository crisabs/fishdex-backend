import factory

from inventory.models import FisherItem
from factory.declarations import SubFactory
from factory.faker import Faker

from inventory.tests.factories.fisher_factory import FisherFactory
from inventory.tests.factories.item_store_factory import ItemStoreFactory


class FisherItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FisherItem

    fisher = SubFactory(FisherFactory)
    item = SubFactory(ItemStoreFactory)
    is_equipped = False
    acquired_at = Faker("date_time_this_year")
    quantity = 1
