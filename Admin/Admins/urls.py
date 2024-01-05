from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.admins_list, name='admin-admins-list'),
    url(r'^add/$', views.admins_add, name='admin-admins-add'),
    url(r'^(?P<admin_pk>\d+)/view/$', views.admins_view, name='admin-admins-view'),
    url(r'^(?P<admin_pk>\d+)/edit/$', views.admins_edit, name='admin-admins-edit'),
    url(r'^(?P<admin_pk>\d+)/deactivate/$', views.admins_deactivate, name='admin-admins-deactivate'),
    url(r'^(?P<admin_pk>\d+)/activate/$', views.admins_activate, name='admin-admins-activate'),
    url(r'^(?P<admin_pk>\d+)/set-password/$', views.admins_set_password, name='admin-admins-set-password'),
]
