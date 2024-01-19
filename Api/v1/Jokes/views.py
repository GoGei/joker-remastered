from rest_framework import viewsets, mixins, renderers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.Utils.Api.mixins import MappedSerializerVMixin
from .serializers import JokeSerializer, LikedJokesSerializer
from core.Joke.models import Joke


class JokesViewSet(MappedSerializerVMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Joke.objects.active().order_by('slug')
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = JokeSerializer


# provide renderer as mixin
# add swagger
class LikedJokesViewSet(MappedSerializerVMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Joke.objects.active().annotate_likes().order_by('likes_annotated', 'slug')
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = LikedJokesSerializer

    @action(detail=False, methods=['get'], url_path='render', url_name='render-list',
            renderer_classes=(renderers.TemplateHTMLRenderer,))
    def render_list(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        jokes = response.data.get('results')
        return Response({'jokes': jokes}, template_name='Api/joke_list.html')

    @action(detail=False, methods=['get'], url_path='render-items', url_name='render-items',
            renderer_classes=(renderers.TemplateHTMLRenderer,),
            pagination_class=None, filter_backends=None)
    def render_items(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            ids = map(int, request.GET.getlist('jokes', []))
        except ValueError:
            ids = []

        jokes = queryset.filter(id__in=ids)
        return Response({'jokes': jokes}, template_name='Api/joke_items.html')

    @action(detail=True, methods=['get'], url_path='render', url_name='render-retrieve',
            renderer_classes=(renderers.TemplateHTMLRenderer,))
    def render_retrieve(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        joke = response.data
        return Response({'joke': joke}, template_name='Api/joke_card.html')
