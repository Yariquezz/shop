from django.contrib import admin
from .models import Category, Products


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "discount",
        "rating",
        "updated_on",
        "created_on",
        "category",
        "description",
        "content",
        "status",
        "image_1",
        "image_2",
        "image_3",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
