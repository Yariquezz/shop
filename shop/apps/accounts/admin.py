from django.contrib import admin
from .models import Customer, DiscountCard


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "address",
        "discount_card"
    )
    search_fields = [
        "user",
        "phone",
        "address",
        "discount_card"
    ]


class DiscountCardAdmin(admin.ModelAdmin):
    list_display = (
        "card_no",
        "benefits",
    )
    search_fields = [
        "card_no",
    ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(DiscountCard, DiscountCardAdmin)
