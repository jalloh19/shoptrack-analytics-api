from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ("id", "added_at", "updated_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "user__username")
    readonly_fields = ("id", "created_at", "updated_at")
    inlines = [CartItemInline]

    fieldsets = (
        ("Cart Information", {"fields": ("user", "status")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at", "abandoned_at", "purchased_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "quantity", "added_at")
    list_filter = ("added_at",)
    search_fields = ("product__name", "cart__user__email")
    readonly_fields = ("id", "added_at", "updated_at")
