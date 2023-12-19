from django.shortcuts import render


def home_index(request):
    return render(request, 'Admin/home_index.html')
