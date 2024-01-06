from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.activity_log_list, name='admin-logger-list'),
    url(r'objects/$', views.activity_log_objects_list, name='admin-logger-objects-list'),
]
