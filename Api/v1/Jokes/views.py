from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.Joke.models import Joke, JokeSeen, JokeLikeStatus
from . import base_views
from .filters import AccountJokesFilter
from .serializers import JokeSerializer, LikedJokesSerializer, AccountJokesSerializer


class JokesViewSet(base_views.JokesReadOnlyRenderViewSet):
    queryset = Joke.objects.active().annotate_likes().order_by('-likes_annotated')
    permission_classes = (AllowAny,)
    serializer_class = LikedJokesSerializer
    serializer_map = {
        'get_daily_jokes': JokeSerializer
    }
    empty_serializers = ('clear_seen_daily_jokes',)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            qs = qs.annotate_is_liked_by_user(user)
        return qs

    @action(detail=False, methods=['get'], url_path='get-daily-joke', url_name='get-daily-joke',
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
                cache.set('seen_jokes', seen_jokes, settings.JOKES_CACHE_TTL)

        if not joke:
            response = {'text': _('There are no more jokes for today!')}
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(self.get_serializer(instance=joke).data)

    @action(detail=False, methods=['post'], url_path='clear-seen-daily-jokes', url_name='clear-seen-daily-jokes')
    def clear_seen_daily_jokes(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            JokeSeen.objects.filter(user=user).delete()
            JokeLikeStatus.objects.filter(user=user).delete()
        else:
            cache.delete('seen_jokes')
        return Response(status=status.HTTP_200_OK)


class AccountBaseJokesViewSet(base_views.JokesReadOnlyRenderViewSet):
    queryset = Joke.objects.active().annotate_likes()
    # serializer_class = AccountJokesSerializer
    serializer_class = LikedJokesSerializer

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return self.queryset.none()

        qs = super().get_queryset()
        qs = qs.annotate_is_liked_by_user(user=user)
        qs = qs.ordered()
        return qs


class AccountJokesViewSet(AccountBaseJokesViewSet):
    empty_serializers = ('like', 'dislike', 'deactivate')

    filter_backends = AccountBaseJokesViewSet.filter_backends + (DjangoFilterBackend,)
    filterset_class = AccountJokesFilter

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def dislike(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.dislike(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deactivate(request.user)
        return Response(status=status.HTTP_200_OK)


class FavouriteJokesViewSet(AccountBaseJokesViewSet):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.liked_by_user(self.request.user)
        qs = qs.ordered()
        return qs


class SeenJokesViewSet(AccountBaseJokesViewSet):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.seen_by_user(self.request.user)
        qs = qs.ordered_by_is_liked_by_user('-likes_annotated')
        return qs
