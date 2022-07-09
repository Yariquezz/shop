from unicodedata import category
from django.http import JsonResponse
from django.views import generic
from .models import Products, Category
from apps.carts.models import Cart, CartItems
from apps.orders.models import Warehouse
from apps.blog.models import Blog
from apps.about.models import About
from apps.accounts.models import Customer
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Sum
from django.conf import settings
import logging
import uuid
import requests


logger = logging.getLogger(__name__)


class ProductsList(generic.ListView):
    queryset = Products.objects.filter(status=1)
    template_name = 'products/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            customer = self.request.user.customer
        except Exception as err:
            logger.error(err)
            self.request.session.setdefault(
                'device',
                str(uuid.uuid4())
            )
            device = self.request.COOKIES.get(
                'device'
            )
            customer, created = Customer.objects.get_or_create(
                device=device
            )
        cart, created = Cart.objects.get_or_create(
            customer=customer,
            is_ordered=False,
        )
        categories = Category.objects.all()
        context['categories'] = categories
        if cart:
            context['cart'] = cart
            context['cart_items'] = CartItems.objects.filter(
                cart=cart
            )
            quantity = CartItems.objects.filter(
                cart=cart
            ).aggregate(Sum('quantity'))
            context['items_quantity'] = quantity['quantity__sum']

        return context


def filter(request, *args, **kwargs):
    if request.method == 'POST':
        products_list = Products.objects.filter(
            category__in=Category.objects.filter(
                name__in=request.POST.getlist('products')
            )
        )
    else:
        products_list = Products.objects.filter(status=1)
    context = dict(
        products_list=products_list,
        fltr_items=Category.objects.all(),
    )
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
    context['cart'] = cart
    context['cart_items'] = CartItems.objects.filter(
        cart=cart
    )
    quantity = CartItems.objects.filter(
        cart=cart
    ).aggregate(Sum('quantity'))
    context['items_quantity'] = quantity['quantity__sum']

    return render(request, 'products/shop.html', context)


class ProductDetail(generic.DetailView):
    model = Products
    template_name = 'products/product_detail.html'

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
        context['cart'] = cart
        context['cart_items'] = CartItems.objects.filter(
            cart=cart
        )
        quantity = CartItems.objects.filter(
            cart=cart
        ).aggregate(Sum('quantity'))
        context['items_quantity'] = quantity['quantity__sum']
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
                object_list = Products.objects.filter(category__in=category)
        return object_list


def add_to_cart(request, product_code):
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

    return redirect('products:products')

def home(request):
   
    try:
        customer = request.user.customer
    except Exception as err:
        logger.error(err)
        request.session.setdefault(
            'device',
            str(uuid.uuid4())
        )
        device = request.COOKIES.get(
            'device'
        )
        customer, created = Customer.objects.get_or_create(
            device=device
        )
    cart, created = Cart.objects.get_or_create(
        customer=customer,
        is_ordered=False,
    )
    context = dict(
        blog_posts=Blog.objects.filter(status=1),
        info=About.objects.filter(status=1),
        products=Products.objects.filter(status=1),
        categories=Category.objects.all(),
        cart=cart,
        cart_items=CartItems.objects.filter(
            cart=cart
        )
    )

    quantity = CartItems.objects.filter(
        cart=cart
    ).aggregate(Sum('quantity'))
    context['items_quantity'] = quantity['quantity__sum']
    return render(request, 'products/index.html', context)
    



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
