from django.contrib import admin

from inventory.models import FisherFish, FisherItem


@admin.register(FisherFish)
class FisherFishAdmin(admin.ModelAdmin):
    list_display = (
        "fisher",
        "fish",
        "pk",
        "caught_at",
        "weight",
        "length",
        "description",
    )
    list_filter = ("weight", "caught_at")
    search_fields = ("fisher__nickname",)
    readonly_fields = ("fisher",)


@admin.register(FisherItem)
class FisherItemAdmin(admin.ModelAdmin):
    list_display = ("fisher", "item", "is_equipped", "acquired_at", "quantity")
    list_filter = ("is_equipped",)
    search_fields = ("fisher__nickname",)
    readonly_fields = ("fisher",)
