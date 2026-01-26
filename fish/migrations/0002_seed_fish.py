from django.db import migrations


def seed_fish(apps, schema_editor):
    Fish = apps.get_model("fish", "Fish")

    fishes = [
        {
            "fish_id": 1,
            "name": "Salmon",
            "description": "A strong migratory fish known for swimming upstream.",
            "habitat": "RIVER",
            "rarity": "COMMON",
            "base_weight": 3.0,
            "base_price": 15,
        },
        {
            "fish_id": 2,
            "name": "Trout",
            "description": "A fast freshwater fish prized by anglers.",
            "habitat": "RIVER",
            "rarity": "COMMON",
            "base_weight": 1.5,
            "base_price": 12,
        },
        {
            "fish_id": 3,
            "name": "Catfish",
            "description": "A large bottom-dwelling fish with whisker-like barbels.",
            "habitat": "RIVER",
            "rarity": "COMMON",
            "base_weight": 5.0,
            "base_price": 20,
        },
        {
            "fish_id": 4,
            "name": "Pike",
            "description": "An aggressive predator with sharp teeth.",
            "habitat": "RIVER",
            "rarity": "RARE",
            "base_weight": 6.0,
            "base_price": 35,
        },
        {
            "fish_id": 5,
            "name": "Sturgeon",
            "description": "An ancient fish species valued for its size and roe.",
            "habitat": "RIVER",
            "rarity": "LEGENDARY",
            "base_weight": 20.0,
            "base_price": 120,
        },
        {
            "fish_id": 6,
            "name": "Perch",
            "description": "A common lake fish with distinctive stripes.",
            "habitat": "LAKE",
            "rarity": "COMMON",
            "base_weight": 1.0,
            "base_price": 8,
        },
        {
            "fish_id": 7,
            "name": "Carp",
            "description": "A hardy fish known for its size and adaptability.",
            "habitat": "LAKE",
            "rarity": "COMMON",
            "base_weight": 4.0,
            "base_price": 14,
        },
        {
            "fish_id": 8,
            "name": "Bluegill",
            "description": "A small and colorful freshwater fish.",
            "habitat": "LAKE",
            "rarity": "COMMON",
            "base_weight": 0.8,
            "base_price": 6,
        },
        {
            "fish_id": 9,
            "name": "Largemouth Bass",
            "description": "A popular sport fish with powerful strikes.",
            "habitat": "LAKE",
            "rarity": "RARE",
            "base_weight": 3.5,
            "base_price": 30,
        },
        {
            "fish_id": 10,
            "name": "Northern Pike",
            "description": "A large apex predator lurking in lake vegetation.",
            "habitat": "LAKE",
            "rarity": "LEGENDARY",
            "base_weight": 10.0,
            "base_price": 90,
        },
        {
            "fish_id": 16,
            "name": "Clownfish",
            "description": "A small reef fish living among sea anemones.",
            "habitat": "OCEAN",
            "rarity": "COMMON",
            "base_weight": 0.3,
            "base_price": 12,
        },
        {
            "fish_id": 17,
            "name": "Angelfish",
            "description": "A brightly colored reef-dwelling fish.",
            "habitat": "OCEAN",
            "rarity": "COMMON",
            "base_weight": 0.6,
            "base_price": 15,
        },
        {
            "fish_id": 18,
            "name": "Great White Shark",
            "description": "A massive apex predator of the open ocean.",
            "habitat": "OCEAN",
            "rarity": "RARE",
            "base_weight": 700.0,
            "base_price": 400,
        },
        {
            "fish_id": 19,
            "name": "Manta Ray",
            "description": "A gentle giant gliding through ocean waters.",
            "habitat": "OCEAN",
            "rarity": "RARE",
            "base_weight": 900.0,
            "base_price": 450,
        },
        {
            "fish_id": 20,
            "name": "Blue Whale",
            "description": "The largest animal ever known to exist.",
            "habitat": "OCEAN",
            "rarity": "LEGENDARY",
            "base_weight": 120000.0,
            "base_price": 1000,
        },
    ]

    for data in fishes:
        Fish.objects.get_or_create(fish_id=data["fish_id"], defaults=data)


class Migration(migrations.Migration):
    dependencies = [
        ("fish", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_fish),
    ]
