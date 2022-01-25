from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('last_cart', views.LastCartView.as_view(), name='last_cart'),
    path('delete/<str:product_code>', views.delete_item, name='delete'),
    path('add/<str:product_code>', views.add_item, name='add'),
]
