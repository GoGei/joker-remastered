from rest_framework import serializers
from core.Joke.models import Joke


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = (
            'id',
            'text',
        )


class AccountJokesSerializer(JokeSerializer):
    is_liked = serializers.BooleanField(source='is_liked_by_user_annotated', read_only=True, allow_null=True)

    class Meta(JokeSerializer.Meta):
        model = Joke
        fields = read_only_fields = JokeSerializer.Meta.fields + ('is_liked',)


class LikedJokesSerializer(AccountJokesSerializer):
    likes = serializers.IntegerField(source='likes_annotated', read_only=True)

    class Meta(JokeSerializer.Meta):
        model = Joke
        fields = read_only_fields = AccountJokesSerializer.Meta.fields + ('likes',)


class JokeSendViaEmailSerializer(serializers.Serializer):
    receiver = serializers.EmailField()

    def validate_receiver(self, receiver: str):
        return receiver.strip()
