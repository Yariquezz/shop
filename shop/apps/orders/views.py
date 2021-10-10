from .models import Order
from apps.carts.models import Cart, CartItems
from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


class OrdersView(generic.ListView):
    queryset = Order.objects.all()
    template_name = 'orders/order.html'


class EditOrder(generic.UpdateView):
    model = Order
    # form_class = EditPostForm
    fields = [
        "shipping_address",
        "payment",
        "shipped",
    ]
    template_name = 'orders/create_order.html'


def create_order(request, *args, **kwargs):
    try:
        cart = Cart.objects.filter(
            user=request.user,
            is_ordered=False,
        ).first()
        cart.is_ordered = True
        order = Order.objects.create(
            cart=cart,
        )
        cart.save()
        order.save()
    except Exception as err:
        logger.error(err)
        messages.error(request, err)
    return redirect('orders:edit_order', pk=order.id)


def order_details(request, **kwargs):
    order = Order.objects.filter(
        public_id=kwargs.get('public_id')
    ).first()
    order_items = CartItems.objects.filter(
        cart=order.cart,
    )
    context = {}
    context['order'] = order
    context['order_items'] = order_items
    total = 0
    for item in order_items:
        total += item.amount
    context['total'] = total

    return render(request, 'orders/order_detail.html', context)


class OrderDetailsView(generic.DetailView):
    model = Order
    template_name = 'orderss/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_items'] = Order.objects.all()
        context['order_items'] = CartItems.objects.all()
        return context
