from django.db import migrations


def seed_item(apps, schema_editor):
    ItemStore = apps.get_model("store", "ItemStore")

    items = [
        {"name": "Basic Rod", "type": "ROD", "price": 100, "effect": 0.3},
        {"name": "Super Rod", "type": "ROD", "price": 300, "effect": 0.45},
        {"name": "Ultra Rod", "type": "ROD", "price": 800, "effect": 0.85},
        {"name": "Basic Bait", "type": "BAIT", "price": 50, "effect": 0.05},
        {"name": "Super Bait", "type": "BAIT", "price": 100, "effect": 0.1},
        {"name": "Ultra Bait", "type": "BAIT", "price": 200, "effect": 0.15},
    ]

    for data in items:
        ItemStore.objects.get_or_create(
            name=data["name"],
            defaults=data,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_item),
    ]
