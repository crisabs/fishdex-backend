import factory

from store.models import ItemStore


class ItemStoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ItemStore

    name = "Basic Rod"
    code = "ROD_BASIC"
    tyoe = "ROD"
    price = 100
    effect = 1.3
