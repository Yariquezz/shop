from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, UserForm
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)


def login_form(request):
    list(messages.get_messages(request))
    print(request.session.session_key)
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logging.info(f'User {user} logged in')
                    return redirect('/')
            else:
                logging.info('Invalid password or username')
                messages.warning(
                    request,
                    "Invalid password or username"
                )

    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, 'accounts/login.html', context)


def register_form(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            new_user = User.objects.create_user(
                user_form.cleaned_data['username'],
                user_form.cleaned_data['email'],
                user_form.cleaned_data['password'],
            )
            new_user.save()
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('/')
        messages.warning(
            request,
            "Unsuccessful registration. Invalid information"
        )

    form = UserForm()
    context = {
        "form": form,
    }
    return render(request, 'accounts/register.html', context)


def logout_form(request):
    logout(request)
    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, 'accounts/login.html', context)
