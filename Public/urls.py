from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url(r'^', include('Public.Home.urls')),
    url(r'^account/', include('Public.Account.urls')),
]
