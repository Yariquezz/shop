from django.contrib import admin
from .models import Order


class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "shipping_address",
        "payment",
        "shipped",
    )
    search_fields = [
        "cart",
    ]


admin.site.register(Order, OrdersAdmin)
