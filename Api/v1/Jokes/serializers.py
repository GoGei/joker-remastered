from rest_framework import serializers
from core.Joke.models import Joke


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = (
            'id',
            'text',
        )


class LikedJokesSerializer(JokeSerializer):
    likes = serializers.IntegerField(source='likes_annotated', read_only=True)

    class Meta(JokeSerializer.Meta):
        model = Joke
        fields = JokeSerializer.Meta.fields + ('likes',)
