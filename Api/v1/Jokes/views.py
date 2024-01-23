from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
    # authentication_classes = ()
    serializer_class = JokeSerializer
    empty_serializers = ('clear_seen_jokes',)

    @action(detail=False, methods=['get'], url_path='daily-joke', url_name='daily-joke',
            pagination_class=None, filter_backends=None)
    def get_daily_jokes(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()

        if user.is_authenticated:
            jokes = queryset.not_seen_by_user(user=user).order_by('?')
            joke = jokes.first()
            if joke:
                joke.make_seen(user)
        else:
            seen_jokes = cache.get('seen_jokes', [])
            queryset = self.get_queryset()
            if seen_jokes:
                try:
                    queryset = queryset.exclude(id__in=seen_jokes)
                except ValueError:
                    queryset = queryset.none()

            joke = queryset.order_by('?').first()
            if joke:
                seen_jokes.append(joke.pk)
                cache.set('seen_jokes', seen_jokes)

        if not joke:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(JokeSerializer(instance=joke).data, status=status.HTTP_200_OK)


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
