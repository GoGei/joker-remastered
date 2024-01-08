from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_hosts import reverse

from core.Utils.Access.decorators import manager_required, superuser_required
from core.User.models import User
from .forms import AdminsFilterForm, AdminAddForm, AdminEditForm, AdminSetPasswordForm
from .tables import AdminTable

from core.Utils.Logger.logger import log


def get_base_qs():
    return User.objects.managers().order_by('email')


@manager_required
def admins_list(request):
    users = get_base_qs()

    user_filter = AdminsFilterForm(request.GET, queryset=users)
    users = user_filter.qs
    table_body = AdminTable(users, request=request)

    table = {
        'body': table_body,
        'filter': {
            'body': user_filter,
            'action': reverse('admin-admins-list', host='admin'),
        }
    }

    return render(request, 'Admin/Admins/admins_list.html',
                  {'table': table})


@manager_required
def admins_view(request, admin_pk):
    admin = get_object_or_404(get_base_qs(), pk=admin_pk)
    return render(request, 'Admin/Admins/admins_view.html', {'admin': admin})


@superuser_required
def admins_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-admins-list', host='admin'))

    form_body = AdminAddForm(request.POST or None)

    if form_body.is_valid():
        admin = form_body.save()
        msg = _(f'Admin {admin.label} added')
        messages.success(request, msg)
        log.object('admin_add', msg,
                   instance=admin,
                   user=request.user)
        return redirect(reverse('admin-admins-set-password', args=[admin.id], host='admin'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Admin/Admins/admins_add.html',
                  {'form': form})


@superuser_required
def admins_edit(request, admin_pk):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-admins-list', host='admin'))

    admin = get_object_or_404(get_base_qs(), pk=admin_pk)
    initial = model_to_dict(admin)
    form_body = AdminEditForm(request.POST or None, instance=admin, initial=initial)

    if form_body.is_valid():
        admin = form_body.save()
        msg = _(f'Admin {admin.label} edited')
        messages.success(request, msg)
        log.object('admin_edit', msg,
                   instance=admin,
                   user=request.user)
        return redirect(reverse('admin-admins-view', args=[admin.id], host='admin'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Admin/Admins/admins_edit.html',
                  {'form': form, 'admin': admin})


@superuser_required
def admins_deactivate(request, admin_pk):
    admin = get_object_or_404(get_base_qs(), pk=admin_pk)
    admin.is_active = False
    admin.save()

    msg = _(f'Admin {admin.label} deactivated')
    messages.success(request, msg)
    log.object('admin_deactivate', msg,
               instance=admin,
               user=request.user)
    return redirect(reverse('admin-admins-list', host='admin'))


@superuser_required
def admins_activate(request, admin_pk):
    admin = get_object_or_404(get_base_qs(), pk=admin_pk)
    admin.is_active = True
    admin.save()

    msg = _(f'Admin {admin.label} activated')
    messages.success(request, msg)
    log.object('admin_activate', msg,
               instance=admin,
               user=request.user)
    return redirect(reverse('admin-admins-list', host='admin'))


@superuser_required
def admins_set_password(request, admin_pk):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-admins-list', host='admin'))

    admin = get_object_or_404(get_base_qs(), pk=admin_pk)
    form_body = AdminSetPasswordForm(request.POST or None, instance=admin)

    if form_body.is_valid():
        admin = form_body.save()

        msg = _(f'Admin {admin.label} set password')
        messages.success(request, msg)
        log.object('admin_set_password', msg,
                   instance=admin,
                   user=request.user)
        return redirect(reverse('admin-admins-view', args=[admin.id], host='admin'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Admin/Admins/admins_edit.html',
                  {'form': form, 'admin': admin})
