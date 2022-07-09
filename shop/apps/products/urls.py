from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path(
        'filter/',
        views.filter,
        name='filter'
    ),
    path(
        'search/',
        views.SearchResultsView.as_view(),
        name='search_results'
    ),
    path(
        'get_warehouses/',
        views.get_warehouses,
        name='get_warehouses'
    ),
    path(
        'refresh_warehouses/',
        views.refresh_warehouses,
        name='refresh_warehouses'
    ),
    path(
        '',
        views.home,
        name='home'
    ),
    path(
        'products/',
        views.ProductsList.as_view(),
        name='products'
    ),
    path(
        'products/<slug:slug>',
        views.ProductDetail.as_view(),
        name='product_detail'
    ),
    path(
        'add_to_cart/<str:product_code>',
        views.add_to_cart,
        name='add_to_cart'
    )
]
