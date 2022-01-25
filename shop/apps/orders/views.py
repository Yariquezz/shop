from .models import Order
from .forms import EditOrderForm
from apps.carts.models import Cart, CartItems
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)


class OrdersView(generic.ListView):
    # queryset = Order.objects.all()
    template_name = 'orders/order.html'

    def get_queryset(self):
        empty_orders = Order.objects.filter(
            shipping_address=None
        )
        empty_orders.delete()
        orders = Order.objects.all()
        return orders


class EditOrder(generic.UpdateView):
    model = Order
    form_class = EditOrderForm
    template_name = 'orders/create_order.html'


class OrderDeleteView(generic.DeleteView):
    model = Order
    template_name = 'orders/delete_order.html'
    success_url = reverse_lazy('products:products')


class OrderUpdateView(generic.UpdateView):
    model = Order
    form_class = EditOrderForm
    template_name = 'orders/update_order.html'


def create_order(request):
    try:
        cart = Cart.objects.filter(
            user=request.user,
            is_ordered=False,
        ).first()
        if cart:
            cart.is_ordered = True
        else:
            cart = Cart.objects.filter(
                user=request.user,
                is_ordered=True,
            ).last()
            cart.pk = None
        cart.save()
        order = Order.objects.create(
            cart=cart,
        )
        order.save()
    except Exception as err:
        logger.error(err)
    return redirect('orders:update_order', pk=order.id)


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
