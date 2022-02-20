from django.contrib import admin
from . models import Cart, CartItems


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "customer",
        "updated",
        "timestamp",
        "is_ordered"
    )
    list_filter = (
        "updated",
        "timestamp"
    )
    search_fields = [
        "customer",
    ]


class CartItemsAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
    )
    list_filter = (
        "cart",
        "product",
    )
    search_fields = [
        "customer",
    ]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)
