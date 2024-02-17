from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login/$', views.login_view, name='admin-login'),
    url(r'logout/$', views.logout_view, name='admin-logout'),

    url(r'forgot-password/$', views.forgot_password_view, name='admin-forgot-password'),
    url(r'forgot-password/success/$', views.forgot_password_success_view, name='admin-forgot-password-success'),
    url(r'forgot-password/confirm/(?P<key>.*)$', views.forgot_password_confirm_view,
        name='admin-forgot-password-confirm'),
]
