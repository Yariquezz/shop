from django.shortcuts import render
from apps.products.models import Products


def payment(request, *args, **kwargs):
    if request.user.is_authenticated:
        products = Products.objects.all()
        userName = request.user.username
        userMail = request.user.email
        context = {
            'products': products,
            'userName': userName,
            'userMail': userMail,
        }
    return render(request, 'payments/payment.html', context)
