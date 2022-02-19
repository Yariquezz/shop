from django.shortcuts import redirect
from .models import CartItems, Cart
from apps.accounts.models import Customer
from apps.products.models import Products
from django.views import generic
import logging

logger = logging.getLogger(__name__)


class CartView(generic.list.ListView):

    template_name = 'carts/cart.html'

    def get_queryset(self):
        try:
            customer = self.request.user.customer
        except Exception as err:
            logger.error(err)
            device = self.request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(
                device=device
            )
        cart, created = Cart.objects.get_or_create(
            customer=customer,
            is_ordered=False,
        )
        items = CartItems.objects.filter(
            cart=cart,
        )
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            customer = self.request.user.customer
        except Exception as err:
            logger.error(err)
            device = self.request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(
                device=device
            )
        cart, created = Cart.objects.get_or_create(
            customer=customer,
            is_ordered=False,
        )
        items = CartItems.objects.filter(
            cart=cart,
        )
        total = 0
        for item in items:
            total += item.amount
        context['total'] = total

        return context


def add_item(request, product_code):
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
    product = Products.objects.get(
        product_code=product_code
    )
    cart_item = CartItems.objects.get(
        cart=cart,
        product=product,
    )
    cart_item.quantity += 1
    cart_item.save()
    return redirect('carts:cart')


def delete_item(request, product_code):
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
    product = Products.objects.get(
        product_code=product_code
    )
    cart_item = CartItems.objects.get(
        cart=cart,
        product=product,
    )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    if CartItems.objects.count() < 1:
        return redirect('products:products')

    return redirect('carts:cart')
