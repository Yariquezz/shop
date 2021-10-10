from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import CartItems, Cart, UserProxy
from apps.products.models import Products
from django.views import generic
import logging

logger = logging.getLogger(__name__)


class CartView(generic.list.ListView):

    template_name = 'carts/cart.html'

    def get_queryset(self):
        cart = Cart.objects.filter(
            user=self.request.user,
            is_ordered=False,
        ).first()
        items = CartItems.objects.filter(
            cart=cart,
        )
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.filter(
                user=self.request.user,
                is_ordered=False,
            ).first()
            items = CartItems.objects.filter(
                cart=cart,
            )
            total = 0
            for item in items:
                total += item.amount
            context['total'] = total

        except Exception as err:
            logger.error(err)

        return context


@login_required
def add_item(request, product_code):
    try:
        cart = Cart.objects.filter(
            user=request.user,
            is_ordered=False,
        ).first()
        product = Products.objects.get(
            product_code=product_code
        )
        cart_item = CartItems.objects.get(
            cart=cart,
            product=product,
        )
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Add item!")
    except Exception as err:
        logger.error(err)
        messages.error(request, err)
    return redirect('carts:cart')


@login_required
def delete_item(request, product_code):
    try:
        cart = Cart.objects.filter(
            user=request.user,
            is_ordered=False,
        ).first()
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
            messages.success(request, "Item removed!")
        if CartItems.objects.count() < 1:
            return redirect('products:products')
    except Exception as err:
        logger.error(err)
        messages.error(request, err)

    return redirect('carts:cart')
