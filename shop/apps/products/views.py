from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Products
from apps.carts.models import Cart, CartItems
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q, Sum
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)


class ProductsList(generic.ListView):
    queryset = Products.objects.filter(status=1).order_by('-created_on')
    template_name = 'products/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.filter(
                user=self.request.user,
                is_ordered=False,
            )
            context['cart'] = cart
            context['cart_items'] = CartItems.objects.filter(
                cart=cart[0]
            )
            quantity = CartItems.objects.filter(
                cart=cart[0]
            ).aggregate(Sum('quantity'))
            context['items_quantity'] = quantity['quantity__sum']
        except Exception as err:
            logger.error(err)

        return context


class ProductDetail(generic.DetailView):
    model = Products
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.filter(
                user=self.request.user,
                is_ordered=False,
            )
            context['cart'] = cart
            context['cart_items'] = CartItems.objects.filter(
                cart=cart[0]
            )
            quantity = CartItems.objects.filter(
                cart=cart[0]
            ).aggregate(Sum('quantity'))
            context['items_quantity'] = quantity['quantity__sum']
        except Exception as err:
            logger.error(err)

        return context


class SearchResultsView(generic.ListView):
    model = Products
    template_name = 'products/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Products.objects.filter(
            Q(description__icontains=query) | Q(title__icontains=query))
        return object_list


@login_required
def add_to_cart(request, product_code):
    try:
        cart = Cart.objects.filter(
            user=request.user,
            is_ordered=False,
        ).first()
        if not cart:
            cart = Cart.objects.create(
                user=request.user,
            )

        product = get_object_or_404(
            Products,
            product_code=product_code
        )

        cart_item, created = CartItems.objects.get_or_create(
            cart=cart,
            product=product
        )
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Cart updated!")
    except Exception as err:
        logger.error(err)
        messages.error(request, err)
    return redirect('products:products')
