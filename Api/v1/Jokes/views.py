from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.Utils.Api.mixins import MappedSerializerVMixin
from .serializers import JokeSerializer
from core.Joke.models import Joke


class JokesViewSet(MappedSerializerVMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Joke.objects.active().order_by('slug')
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = JokeSerializer
