from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, UserForm
from django.contrib import messages
from shop.celery import send_confirmation_email
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .tokens import account_activation_token
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
            new_user.is_active = False
            new_user.save()
            current_site = get_current_site(request)
            message = render_to_string(
                'email_template.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(
                        force_bytes(
                            new_user.pk
                        )
                    ),
                    'token': account_activation_token.make_token(
                        new_user
                    ),
                })
            send_confirmation_email(
                subject=new_user.email,
                message=message
            )
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


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')
