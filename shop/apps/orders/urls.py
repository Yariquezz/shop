from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path(
        '',
        views.OrdersView.as_view(),
        name='orders'
    ),
    path(
        'order/',
        views.create_order,
        name='create_order'
    ),
    path(
        'edit/<int:pk>/',
        views.EditOrder.as_view(),
        name='edit_order'
    ),
    path(
        'update/<int:pk>/',
        views.OrderUpdateView.as_view(),
        name='update_order'
    ),
    path(
        'delete/<int:pk>/',
        views.OrderDeleteView.as_view(),
        name='delete_order'
    ),
    path(
        '<str:public_id>/',
        views.order_details,
        name='orders_details'
    ),
]
