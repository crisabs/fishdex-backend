from fish.models import Fish
from fishers.models import Fisher
from django.db import models

from store.models import ItemStore


class FisherFish(models.Model):
    fisher = models.ForeignKey(
        Fisher, on_delete=models.CASCADE, related_name="caught_fish"
    )
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, related_name="owners")
    caught_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(blank=True, null=True, max_length=50)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["-caught_at"]


class FisherItem(models.Model):
    fisher = models.ForeignKey(Fisher, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(ItemStore, on_delete=models.CASCADE, related_name="owners")
    is_equipped = models.BooleanField(default=False)
    acquired_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveBigIntegerField(default=1)

    class Meta:
        unique_together = ("fisher", "item")
