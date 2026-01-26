from django.db import models


class Habitat(models.TextChoices):
    RIVER = "RIVER", "River"
    LAKE = (
        "LAKE",
        "Lake",
    )
    SEA = "SEA", "Sea"
    OCEAN = "OCEAN", "Ocean"


class Rarity(models.TextChoices):
    COMMON = "COMMON", "Common"
    RARE = "RARE", "Rare"
    LEGENDARY = "LEGENDARY", "Legendary"


class Fish(models.Model):
    name = models.CharField(max_length=30, unique=True)
    fish_id = models.PositiveIntegerField(default=1, unique=True)
    description = models.CharField(max_length=100)
    habitat = models.CharField(
        max_length=15, choices=Habitat.choices, default=Habitat.RIVER
    )
    rarity = models.CharField(
        max_length=15, choices=Rarity.choices, default=Rarity.COMMON
    )
    base_weight = models.FloatField(default=0.0)
    base_price = models.PositiveIntegerField(default=10)

    def __str__(self) -> str:
        return f"{self.fish_id} {self.name}"
