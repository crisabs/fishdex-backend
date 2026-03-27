from django.contrib import admin
from store.models import ItemStore


@admin.register(ItemStore)
class ItemStoreAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price", "effect")
    search_fields = ("name", "type", "price", "effect")
    readonly_fields = ("name",)
