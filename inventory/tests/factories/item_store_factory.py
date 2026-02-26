import factory

from store.models import ItemStore


class ItemStoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ItemStore
        django_get_or_create = ("code",)

    name = "Basic Rod"
    code = "ROD_BASIC"
    type = "ROD"
    price = 100
    effect = 1.3
