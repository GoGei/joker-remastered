from django_hosts import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _

from core.User.senders import AdminForgotPasswordSender
from core.Utils.Access.user_check_functions import manager_check
from .forms import LoginForm, ForgotPasswordForm, ForgotPasswordConfirmForm


def login_view(request):
    user = request.user
    if user.is_authenticated and manager_check(user):
        return redirect(reverse('admin-index', host='admin'))

    initial = {'email': request.COOKIES.get('email', '')}
    form = LoginForm(request.POST or None, initial=initial)
    if form.is_valid():
        data = form.cleaned_data

        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            form.add_error(None, _('User with this email and password not found or inactive'))
        elif (user.is_staff or user.is_superuser) and user.is_active:
            login(request, user)

            remember_me = data.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True

            response = HttpResponseRedirect(reverse('admin-index', host='admin'))
            response.set_cookie('email', user.email)
            return response
        elif not (user.is_staff or user.is_superuser):
            form.add_error(None, _('User is not a staff ot superuser'))
        else:
            form.add_error(None, _('User is not logged in'))

    return render(request, 'Admin/Login/login.html', {'form': form})


def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)
    if form.is_valid():
        form.send_forgot_password()
        return redirect(reverse('admin-forgot-password-success', host='admin'))
    return render(request, 'Admin/Login/forgot_password.html', {'form': form})


def forgot_password_success_view(request):
    return render(request, 'Admin/Login/forgot_password_success.html')


def forgot_password_confirm_view(request, key):
    user = AdminForgotPasswordSender().get(key)
    if not user:
        return render(request, 'Admin/Login/forgot_password_confirm_error.html')
    if not user.is_active or not (user.is_staff or user.is_superuser):
        return render(request, 'Admin/Login/forgot_password_confirm_error.html')

    form = ForgotPasswordConfirmForm(request.POST or None,
                                     key=key, user=user)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(reverse('admin-login', host='admin'))
    else:
        print(form.errors)
    return render(request, 'Admin/Login/forgot_password_confirm.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('admin-login', host='admin'))
