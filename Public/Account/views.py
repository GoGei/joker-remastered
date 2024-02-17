from django_hosts import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from .forms import LoginForm, ForgotPasswordForm, RegisterForm, ForgotPasswordConfirmForm

from core.User.senders import PublicRegistrationEmailSender, PublicForgotPasswordSender


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('home-register-success', host='public'))

    return render(request, 'Public/Account/register.html', {'form': form})


def register_success_view(request):
    return render(request, 'Public/Account/register_success.html')


def register_confirm(request, key):
    sender = PublicRegistrationEmailSender()
    user = sender.get(key)
    if not user:
        return render(request, 'Public/Account/register_confirm_no_user.html')

    if not user.is_active:
        user.is_active = True
        user.save(update_fields=['is_active'])

    login(request, user)
    sender.delete(key)
    return redirect(reverse('home-index', host='public'))


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect(reverse('home-index', host='public'))

    initial = {'email': request.COOKIES.get('email', '')}
    form = LoginForm(request.POST or None, initial=initial)
    if form.is_valid():
        data = form.cleaned_data

        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            form.add_error(None, _('User with this email and password not found or inactive'))
        elif user.is_active:
            login(request, user)

            remember_me = data.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True

            response = HttpResponseRedirect(reverse('home-index', host='public'))
            response.set_cookie('email', user.email)
            return response
        else:
            form.add_error(None, _('User is deactivated'))

    return render(request, 'Public/Account/login.html', {'form': form})


def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)
    if form.is_valid():
        form.send_forgot_password()
        return redirect(reverse('home-forgot-password-success', host='public'))
    return render(request, 'Public/Account/forgot_password.html', {'form': form})


def forgot_password_success_view(request):
    return render(request, 'Public/Account/forgot_password_success.html')


def forgot_password_confirm_view(request, key):
    user = PublicForgotPasswordSender().get(key)
    if not user:
        return render(request, 'Public/Account/forgot_password_confirm_error.html')

    form = ForgotPasswordConfirmForm(request.POST or None,
                                     key=key, user=user)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(reverse('home-index', host='public'))
    return render(request, 'Public/Account/forgot_password_confirm.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('home-index', host='public'))
