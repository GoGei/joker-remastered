from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'register/$', views.register_view, name='home-register'),
    url(r'register/success/$', views.register_success_view, name='home-register-success'),

    url(r'login/$', views.login_view, name='home-login'),
    url(r'logout/$', views.logout_view, name='home-logout'),

    url(r'forgot-password/$', views.forgot_password_view, name='home-forgot-password'),
    url(r'forgot-password/success/$', views.forgot_password_success_view, name='home-forgot-password-success'),
]
