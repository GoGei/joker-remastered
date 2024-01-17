from django_hosts import reverse


def context(request):
    return {
        'EMPTY_PAGE_API_URL': reverse('api-v1:empty-page', host='api')
    }
