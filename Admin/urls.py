from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url('^', include('Admin.Home.urls')),
    url('^', include('Admin.Login.urls')),

    url('^admins/', include('Admin.Admins.urls')),
    url('^users/', include('Admin.Users.urls')),
    url('^jokes/', include('Admin.Jokes.urls')),
    url('^profile/', include('Admin.Profile.urls')),
    url('^logger/', include('Admin.Logger.urls')),
]
