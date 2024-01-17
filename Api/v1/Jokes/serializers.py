from rest_framework import serializers
from core.Joke.models import Joke


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = (
            'id',
            'text',
        )
