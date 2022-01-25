from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import generic
from .models import Products, Category
from apps.carts.models import Cart, CartItems
from apps.orders.models import Warehouse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q, Sum
from django.conf import settings
import logging
import requests


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
            if cart:
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
            if cart:
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
    model = Products, Category
    template_name = 'products/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Products.objects.filter(
            Q(
                description__icontains=query
            ) | Q(
                title__icontains=query
            ) | Q(
                content__icontains=query
            )
        )
        if not object_list:
            category = Category.objects.filter(Q(name__icontains=query))
            if len(category) > 0:
                object_list = Products.objects.filter(category=category)
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
    except Exception as err:
        logger.error(err)
    return redirect('products:products')


def get_warehouses(request):
    warehouse = Warehouse.objects.all()
    title = list(warehouse.values_list("title", flat=True))
    address = list(warehouse.values_list("address", flat=True))
    src = [f"{key} - {value}" for key, value in zip(address, title)]
    return JsonResponse(src, safe=False)


def refresh_warehouses(request):

    api_domain = 'https://api.novaposhta.ua'

    api_path = '/v2.0/json/AddressGeneral/getWarehouses'

    api_data = {
        'modelName': 'AddressGeneral',
        'calledMethod': 'getWarehouses',
        'apiKey': settings.NP_API_KEY
    }
    response = requests.post(api_domain + api_path, json=api_data).json()

    if not response.get('success'):
        raise Exception(','.join(response.get('errors')))

    Warehouse.objects.all().delete()

    warehouses = []

    for item in response.get('data'):

        params = {
            'title': item.get('Description'),
            'address': item.get('CityDescription')
        }

        warehouses.append(Warehouse(**params))

    Warehouse.objects.bulk_create(warehouses)
    return redirect('products:products')
