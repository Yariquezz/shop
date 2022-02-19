from cmath import e
from .models import Order, Warehouse
from .forms import EditOrderForm
from apps.carts.models import Cart, CartItems
from apps.accounts.models import Customer
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import render, redirect
from shop.celery import send_confirmation_email
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


class OrdersView(generic.ListView):
    template_name = 'orders/order.html'

    def get_queryset(self):
        empty_order = Order.objects.filter(shipping_address=None)
        empty_order.delete()
        orders = Order.objects.all()
        return orders


class OrderDeleteView(generic.DeleteView):
    model = Order
    template_name = 'orders/delete_order.html'
    success_url = reverse_lazy('products:products')


class OrderUpdateView(generic.UpdateView):
    model = Order
    form_class = EditOrderForm
    template_name = 'orders/update_order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['warehouses'] = Warehouse.objects.all()
        return context

    def get_success_url(self):
        return reverse('orders:payment', args=[self.kwargs['pk']])


def create_order(request):
    try:
        customer = request.user.customer
    except Exception as err:
        logger.error(err)
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(
            device=device
        )
    cart, created = Cart.objects.get_or_create(
        customer=customer,
        is_ordered=False,
    )
    cart.is_ordered = True
    cart.save()
    order = Order.objects.create(
        cart=cart,
    )
    order.save()
    return redirect('orders:update_order', pk=order.id)


def update_order(request, **kwargs):
    try:
        customer = request.user.customer
    except Exception as err:
        logger.error(err)
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(
            device=device
        )
    order, created = Order.objects.get_or_create(
        pk=kwargs['pk']
    )
    context = dict(
        warehouses=Warehouse.objects.all(),
        order=order
    )
    if request.method == 'POST':
        order.shipping_address = request.POST.get('shipping_address')
        order.save()
        customer.address = order.shipping_address
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.save()
        return redirect('orders:payment', pk=kwargs['pk'])
    else:
        return render(request, 'orders/update_order.html', context)


def order_details(request, **kwargs):
    order = Order.objects.get_or_create(
        public_id=kwargs.get('public_id')
    )
    order_items = CartItems.objects.filter(
        cart=order.cart,
    )
    context = dict(
        order=order,
        order_items=order_items,
    )
    total = 0
    for item in order_items:
        total += item.amount
    context['total'] = total

    return render(request, 'orders/order_detail.html', context)


def pay_order(request, **kwargs):
    order, created = Order.objects.get_or_create(
        pk=kwargs.get('pk')
    )
    try:
        customer = request.user.customer
    except Exception as err:
        logger.error(err)
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(
            device=device
        )
    customer.address = order.shipping_address
    customer.save()

    order_items = CartItems.objects.filter(
        cart=order.cart,
    )
    context = dict(
        order=order,
        order_items=order_items,
    )
    total = 0
    for item in order_items:
        total += item.amount
    context['total'] = total
    if request.method == 'POST':
        order.payment = "Оплачено"
        order.save()
        if customer.user:
            message = render_to_string(
                'orders/email_template.html', {
                    'user': customer.user.username,
                    'order_items': order_items,
                })
            send_confirmation_email(
                subject=customer.user.email,
                message=message
            )
            return redirect('orders:orders')
        else:
            return redirect('products:products')
    return render(request, 'orders/payment.html', context)
