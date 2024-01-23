from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'top/$', views.home_top, name='home-top'),
    url(r'favourite/$', views.home_favourite, name='home-favourite'),
]
