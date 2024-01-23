from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_hosts import reverse


def home_index(request):
    joke_url = reverse('api-v1:jokes-all-get-daily-joke', host='api')
    return render(request, 'Public/index.html', {'joke_url': joke_url})


def home_top(request):
    jokes_url = reverse('api-v1:jokes-all-list', host='api')
    return render(request, 'Public/top.html', {'jokes_url': jokes_url})


@login_required
def home_favourite(request):
    jokes_url = reverse('api-v1:jokes-favourite-list', host='api')
    return render(request, 'Public/favourite.html', {'jokes_url': jokes_url})


@login_required
def home_seen(request):
    jokes_url = reverse('api-v1:jokes-seen-list', host='api')
    return render(request, 'Public/seen.html', {'jokes_url': jokes_url})
