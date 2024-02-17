from django.shortcuts import render
from django_hosts import reverse
from Public.decorators import public_login_required


def home_index(request):
    joke_url = reverse('api-v1:jokes-all-get-daily-joke', host='api')
    clear_seen_jokes_url = reverse('api-v1:jokes-all-clear-seen-daily-jokes', host='api')
    return render(request, 'Public/index.html', {'joke_url': joke_url,
                                                 'clear_seen_jokes_url': clear_seen_jokes_url})


def home_top(request):
    jokes_url = reverse('api-v1:jokes-all-list', host='api')
    return render(request, 'Public/top.html', {'jokes_url': jokes_url})


@public_login_required
def home_favourite(request):
    jokes_url = reverse('api-v1:jokes-favourite-list', host='api')
    return render(request, 'Public/favourite.html', {'jokes_url': jokes_url})


@public_login_required
def home_seen(request):
    jokes_url = reverse('api-v1:jokes-seen-list', host='api')
    return render(request, 'Public/seen.html', {'jokes_url': jokes_url})
