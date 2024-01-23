from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.Utils.Api.mixins import MappedSerializerVMixin
from core.Joke.models import Joke
from . import base_views
from .serializers import JokeSerializer, LikedJokesSerializer


class JokesReadOnlyViewSet(MappedSerializerVMixin, viewsets.ReadOnlyModelViewSet):
    pass


class JokesReadOnlyRenderViewSet(JokesReadOnlyViewSet, base_views.JokesRenderViewSetMixin):
    pass


class JokesViewSet(JokesReadOnlyViewSet):
    queryset = Joke.objects.active().order_by('slug')
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = JokeSerializer


class LikedJokesViewSet(JokesReadOnlyRenderViewSet):
    queryset = JokesViewSet.queryset.annotate_likes().order_by('likes_annotated', 'slug')
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = LikedJokesSerializer


class FavouriteJokesViewSet(JokesReadOnlyRenderViewSet):
    queryset = Joke.objects.active()
    serializer_class = JokeSerializer

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return self.queryset.none()

        qs = super().get_queryset()
        return qs.seen_by_user(user)
