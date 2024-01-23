from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from Api.v1.User.views import UserViewSet
from Api.v1.Jokes import urls as jokes_urls

from Api.v1.Public import urls as public_urls

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users'),
urlpatterns = router_v1.urls

urlpatterns += [
    url(r'^public/', include(public_urls), name='public'),
    url(r'^jokes/', include(jokes_urls), name='jokes'),
]
