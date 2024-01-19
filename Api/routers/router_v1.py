from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from Api.v1.User.views import UserViewSet
from Api.v1.Jokes.views import JokesViewSet, LikedJokesViewSet
from Api.v1.Public import urls as public_urls

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users'),
router_v1.register('jokes', JokesViewSet, basename='jokes'),
router_v1.register('jokes-liked', LikedJokesViewSet, basename='jokes-liked'),
urlpatterns = router_v1.urls

urlpatterns += [
    url(r'^public/', include(public_urls), name='public'),
]
