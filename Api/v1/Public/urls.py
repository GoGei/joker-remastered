from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^empty-page/$', views.empty_page, name='empty-page'),
]
