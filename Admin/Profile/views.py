from django.forms import model_to_dict
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django_hosts import reverse

from core.Utils.Access.decorators import manager_required
from .forms import ProfileForm, ProfileChangePasswordForm


@manager_required
def profile_view(request):
    profile = request.user
    return render(request, 'Admin/Profile/profile_view.html', {'profile': profile})


@manager_required
def profile_edit_view(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-profile-view', host='admin'))

    profile = request.user
    initial = model_to_dict(profile)
    form_body = ProfileForm(request.POST or None, instance=profile, initial=initial)

    if form_body.is_valid():
        form_body.save()
        messages.success(request, _('Profile edited'))
        return redirect(reverse('admin-profile-view', host='admin'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Admin/Profile/profile_edit.html',
                  {'form': form, 'profile': profile})


@manager_required
def profile_change_password_view(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-profile-view', host='admin'))

    profile = request.user
    initial = model_to_dict(profile)
    form_body = ProfileChangePasswordForm(request.POST or None, instance=profile, initial=initial)

    if form_body.is_valid():
        form_body.save()
        update_session_auth_hash(request, profile)
        messages.success(request, _('Profile password changed'))
        return redirect(reverse('admin-profile-view', host='admin'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Admin/Profile/profile_change_password.html',
                  {'form': form, 'profile': profile})
