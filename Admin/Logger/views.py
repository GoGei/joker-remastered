from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_hosts import reverse

from core.Utils.Logger.models import ActivityLog
from core.Utils.Logger.enums import LevelChoices
from core.Utils.Logger.services import log_qs_to_list
from core.Utils.Access.decorators import manager_required
from .forms import LoggerFilterForm
from .tables import LoggerTable, LoggerObjectTable


@manager_required
def activity_log_objects_list(request):
    qs = ActivityLog.objects.filter(level=LevelChoices.OBJECT).order_by('-stamp')

    activity_log_filter = LoggerFilterForm(request.GET, queryset=qs)
    qs = activity_log_filter.qs
    data = log_qs_to_list(qs, fields=LoggerObjectTable.Meta.fields)
    table_body = LoggerObjectTable(data)

    table = {
        'body': table_body,
        'filter': {
            'body': activity_log_filter,
            'action': reverse('admin-logger-objects-list', host='admin'),
        },
        'on_empty': {
            'title': _('No logs yet'),
            'description': _('Please, wait for logs')
        }
    }

    return render(request, 'Admin/Logger/activity_log_objects_list.html',
                  {'table': table})


@manager_required
def activity_log_list(request):
    qs = ActivityLog.objects.all().order_by('-stamp')

    activity_log_filter = LoggerFilterForm(request.GET, queryset=qs)
    qs = activity_log_filter.qs
    data = log_qs_to_list(qs, fields=LoggerTable.Meta.fields)
    table_body = LoggerTable(data)

    table = {
        'body': table_body,
        'filter': {
            'body': activity_log_filter,
            'action': reverse('admin-logger-list', host='admin'),
        },
        'on_empty': {
            'title': _('No logs yet'),
            'description': _('Please, wait for logs')
        }
    }

    return render(request, 'Admin/Logger/activity_log_list.html',
                  {'table': table})
