from django.contrib import admin
from fishers.models import Fisher


@admin.register(Fisher)
class FisherAdmin(admin.ModelAdmin):
    list_display = ("nickname", "user", "level", "coins")
    search_fields = ("nickname", "user")
    readonly_fields = ("user",)
