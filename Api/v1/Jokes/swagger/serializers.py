from rest_framework import serializers


class LikedJokesRenderItemsSerializer(serializers.Serializer):
    jokes = serializers.ListField(child=serializers.IntegerField(), required=False)
