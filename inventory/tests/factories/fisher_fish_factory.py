import factory
from factory.faker import Faker
from factory.declarations import SubFactory
from inventory.models import FisherFish
from inventory.tests.factories.fish_factory import FishFactory
from inventory.tests.factories.fisher_factory import FisherFactory


class FisherFishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FisherFish

    fisher = SubFactory(FisherFactory)
    fish = SubFactory(FishFactory)
    description = Faker("text", max_nb_chars=50)
    weight = Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    length = Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
