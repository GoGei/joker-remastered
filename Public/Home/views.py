from django.shortcuts import render


def home_index(request):
    return render(request, 'Public/index.html')


def home_top(request):
    return render(request, 'Public/top.html')


def home_favourite(request):
    return render(request, 'Public/favourite.html')


def home_account(request):
    return render(request, 'Public/account.html')
