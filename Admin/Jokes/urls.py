from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.jokes_list, name='admin-jokes-list'),
    url(r'top/$', views.jokes_top_list, name='admin-jokes-top-list'),
    url(r'add/$', views.jokes_add, name='admin-jokes-add'),
    url(r'(?P<joke_pk>\d+)/edit/$', views.jokes_edit, name='admin-jokes-edit'),
    url(r'(?P<joke_pk>\d+)/archive/$', views.jokes_archive, name='admin-jokes-archive'),
    url(r'(?P<joke_pk>\d+)/restore/$', views.jokes_restore, name='admin-jokes-restore'),
    url(r'(?P<joke_pk>\d+)/view/$', views.jokes_view, name='admin-jokes-view'),

    url(r'export/$', views.jokes_export, name='admin-jokes-export'),
    url(r'import/$', views.jokes_import, name='admin-jokes-import'),

    url(r'default-fixture/$', views.jokes_default_fixture, name='admin-jokes-default-fixture'),
    url(r'load-default-fixture/$', views.jokes_load_default_fixture, name='admin-jokes-load-default-fixture'),
]
