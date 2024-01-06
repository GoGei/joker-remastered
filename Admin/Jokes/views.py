from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, Func, F
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_hosts import reverse
from rest_framework.renderers import JSONRenderer

from core.Utils.Access.decorators import manager_required
from core.Joke.models import Joke, JokeLikeStatus
from .forms import JokeFilterForm, JokeAddForm, JokeEditForm, JokeImportForm
from .tables import JokesTable, JokesTopTable


@manager_required
def jokes_list(request):
    jokes = Joke.objects.all().ordered()

    joke_filter = JokeFilterForm(request.GET, queryset=jokes)
    jokes = joke_filter.qs
    table_body = JokesTable(jokes)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'body': joke_filter,
            'action': reverse('admin-jokes-list', host='admin'),
        }
    }

    return render(request, 'Admin/Joke/joke_list.html',
                  {'table': table})


@manager_required
def jokes_top_list(request):
    jokes = (
        Joke.objects.active()
        .annotate_likes()
        .exclude(likes_annotated__lte=0)
        .order_by('-likes_annotated', 'slug')
    )
    table_body = JokesTopTable(jokes)

    table = {
        'title': _('Top jokes'),
        'body': table_body,
        'on_empty': {
            'title': _('No top jokes'),
            'description': _('No jokes have positively rated yet'),
        }
    }

    return render(request, 'Admin/Joke/joke_top_list.html',
                  {'table': table})


@manager_required
def jokes_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-jokes-list', host='admin'))

    form_body = JokeAddForm(request.POST or None)

    if form_body.is_valid():
        joke = form_body.save()
        messages.success(request, f'Joke {joke.pk} added')
        return redirect(reverse('admin-jokes-list', host='admin'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Admin/Joke/joke_add.html',
                  {'form': form})


@manager_required
def jokes_edit(request, joke_pk):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-jokes-list', host='admin'))

    joke = get_object_or_404(Joke, pk=joke_pk)
    form_body = JokeEditForm(request.POST or None,
                             instance=joke)

    if form_body.is_valid():
        joke = form_body.save()
        joke.modify(request.user)
        messages.success(request, f'Joke {joke.pk} edited')
        return redirect(reverse('admin-jokes-list', host='admin'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'Admin/Joke/joke_edit.html',
                  {'form': form, 'joke': joke})


@manager_required
def jokes_view(request, joke_pk):
    joke = get_object_or_404(Joke, pk=joke_pk)
    return render(request, 'Admin/Joke/joke_view.html', {'joke': joke})


@manager_required
def jokes_archive(request, joke_pk):
    joke = get_object_or_404(Joke, pk=joke_pk)
    joke.archive(request.user)
    messages.success(request, f'Joke {joke.pk} archived')
    return redirect(reverse('admin-jokes-list', host='admin'))


@manager_required
def jokes_restore(request, joke_pk):
    joke = get_object_or_404(Joke, pk=joke_pk)
    joke.restore(request.user)
    messages.success(request, f'Joke {joke.pk} restored')
    return redirect(reverse('admin-jokes-list', host='admin'))


@manager_required
def jokes_export(request):
    data = Joke.get_data_to_export()
    content = JSONRenderer().render(data)

    response = HttpResponse(content, content_type='application/json')
    filename = 'jokes.json'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Cache-Control'] = 'no-cache'
    return response


@manager_required
def jokes_import(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-jokes-list', host='admin'))

    form_body = JokeImportForm(request.POST or None, request.FILES or None)
    if form_body.is_valid():
        try:
            form_body.run()
            messages.success(request, f'Jokes imported successfully')
            return redirect(reverse('admin-jokes-list', host='admin'))
        except Exception as e:
            form_body.add_error(None, e)

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'Admin/Joke/joke_import.html',
                  {'form': form})
