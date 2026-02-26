import factory
from factory.faker import Faker
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("email")
    password = factory.django.Password("Str0ngP4ssWord!")
