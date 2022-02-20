from django.contrib import admin
from .models import Order, Warehouse


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


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'address']
    search_fields = ['title', 'address']


admin.site.register(Order, OrdersAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
