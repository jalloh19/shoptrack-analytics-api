from django.contrib import admin

from .models import CartEvent


@admin.register(CartEvent)
class CartEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "user", "product", "quantity_changed", "timestamp")
    list_filter = ("event_type", "timestamp")
    search_fields = ("user__email", "product__name", "cart__id")
    readonly_fields = ("id", "timestamp")

    fieldsets = (
        (
            "Event Information",
            {"fields": ("event_type", "quantity_changed", "session_duration_seconds")},
        ),
        ("Relationships", {"fields": ("cart", "user", "product")}),
        ("Metadata", {"fields": ("id", "timestamp"), "classes": ("collapse",)}),
    )
