from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from apps.products.models import Products, Category
from .views import CartView, add_item, delete_item
from .models import Cart, CartItems


class ClassViewTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@gmail.com',
            password='top_secret'
        )
        cat = Category.objects.create(name='test_category')
        cat.save()
        product = Products.objects.create(
            title='Test Product',
            price=1000,
            category=cat,
            content=dict(this='that')
        )
        product.save()
        self.product = product
        cart = Cart.objects.create(
            user=self.user,
        )
        cart.save()
        cart_item = CartItems.objects.create(
            cart=cart,
            product=product,
            quantity=5,
        )
        cart_item.save()
        self.cart_item = cart_item

    def test_carts(self):
        request = self.factory.get(
            path='/carts/',
            follow=True,
        )
        request.user = self.user
        response = CartView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_carts_delete(self):
        request = self.factory.post(
            path=f'/carts/delete/{self.product.product_code}/',
            follow=True,
            secure=True
        )
        request.user = self.user
        response = delete_item(request, self.product.product_code)
        self.assertEqual(response.status_code, 302)

    def test_carts_add(self):
        request = self.factory.post(
            path=f'/carts/add/{self.product.product_code}/',
            follow=True,
            secure=True
        )
        request.user = self.user
        response = add_item(request, self.product.product_code)
        self.assertEqual(response.status_code, 302)
