from django.contrib import admin
from . models import Cart, CartItems, UserProxy


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "user",
        "updated",
        "timestamp",
        "is_ordered"
    )
    list_filter = (
        "updated",
        "timestamp"
    )
    search_fields = [
        "user",
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
        "user",
    ]


class UserProxyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "session",
    )
    search_fields = [
        "user",
    ]


admin.site.register(Cart, CartAdmin)
admin.site.register(UserProxy, UserProxyAdmin)
admin.site.register(CartItems, CartItemsAdmin)
