from django.shortcuts import render
from .models import About


def about(request):
    context = dict(
        stories=About.objects.filter(status=1)
    )
    return render(request, 'about/about.html', context)


def contact(request):
    return render(request, 'about/contact.html')
