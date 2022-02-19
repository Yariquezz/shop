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
        'payment/<int:pk>/',
        views.pay_order,
        name='payment'
    ),
    path(
        'update/<int:pk>/',
        views.update_order,
        name='update_order'
    ),
    path(
        '<str:public_id>/',
        views.order_details,
        name='orders_details'
    ),
]
