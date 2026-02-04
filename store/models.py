from django.db import models


class _ItemType(models.TextChoices):
    ROD = "ROD", "Rod"
    BAIT = "BAIT", "Bait"


class ItemStore(models.Model):
    name = models.CharField()
    code = models.CharField(max_length=50, unique=True, db_index=True)
    type = models.CharField(
        max_length=15, choices=_ItemType.choices, default=_ItemType.BAIT
    )
    price = models.PositiveIntegerField()
    effect = models.FloatField()

    def __str__(self) -> str:
        return f"{self.name} - type: {self.type}"
