from django.contrib import admin
from fish.models import Fish


@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = (
        "fish_id",
        "name",
        "description",
        "habitat",
        "rarity",
        "base_weight",
        "base_price",
    )

    search_fields = ("fish_id", "name", "habitat")
