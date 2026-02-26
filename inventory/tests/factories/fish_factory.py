import factory
from factory.faker import Faker
from fish.models import Fish, Habitat, Rarity


class FishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fish
        django_get_or_create = ("name",)

    name = "Salmon"
    fish_id = 1
    description = Faker("text", max_nb_chars=100)
    habitat = Habitat.RIVER
    rarity = Rarity.COMMON
    base_weight = 1
    base_price = 1
