from django.db import models
from django.conf import settings


class Fisher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="fisher_profile",
    )
    nickname = models.CharField(max_length=30)
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=100)
    current_zone = models.CharField(max_length=20, default="River")

    def __str__(self) -> str:
        return f"{self.nickname} (Lv. {self.level})"
