from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from .serializers import LikedJokesRenderItemsSerializer

LIKED_JOKES_LIST_SCHEMA = swagger_auto_schema(
    responses={
        status.HTTP_200_OK: 'HTML response with list of liked jokes',
    }
)

LIKED_JOKES_ITEMS_SCHEMA = swagger_auto_schema(
    query_serializer=LikedJokesRenderItemsSerializer,
    responses={
        status.HTTP_200_OK: 'HTML response with list of mentioned jokes',
    }
)

LIKED_JOKES_RETRIEVE_SCHEMA = swagger_auto_schema(
    responses={
        status.HTTP_200_OK: 'HTML response with specific joke',
    }
)
