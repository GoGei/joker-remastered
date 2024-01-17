from rest_framework import views
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['get'])
@authentication_classes(())
@permission_classes(())
def empty_page(request):
    return render(request, 'Api/Public/empty_page.html')
