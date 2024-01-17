from django.shortcuts import render
from core.Joke.models import Joke


def home_index(request):
    return render(request, 'Public/index.html')


def home_top(request):
    # jokes = Joke.objects.active().annotate_likes().order_by('likes_annotated', 'slug')
    # return render(request, 'Public/top.html', {'jokes': jokes})
    return render(request, 'Public/top.html')


def home_favourite(request):
    return render(request, 'Public/favourite.html')


def home_account(request):
    return render(request, 'Public/account.html')
