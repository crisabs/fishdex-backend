import factory
from factory.declarations import SubFactory
from factory.faker import Faker


from fishers.models import Fisher
from inventory.tests.factories.user_factory import UserFactory


class FisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fisher

    user = SubFactory(UserFactory)
    nickname = Faker("user_name")
    level = 1
    experience = 0
    coins = 100
    current_zone = "River"
