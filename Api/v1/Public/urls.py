from django.conf.urls import url

from .views import empty_page

urlpatterns = [
    url(r'^empty-page/$', empty_page, name='empty-page'),
]
