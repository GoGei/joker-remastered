from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.profile_view, name='admin-profile-view'),
    url(r'edit/$', views.profile_edit_view, name='admin-profile-edit'),
    url(r'change-password/$', views.profile_change_password_view, name='admin-profile-change-password'),
]
