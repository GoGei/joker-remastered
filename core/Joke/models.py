from typing import List, Dict

from django.db import models
from django.utils import timezone
from django.conf import settings

from core.Utils.Mixins.models import CrmMixin, SlugifyMixin, ExportableMixin


class Joke(CrmMixin, SlugifyMixin, ExportableMixin):
    SLUGIFY_FIELD = 'text'
    text = models.CharField(max_length=4096)

    class Meta:
        db_table = 'joke'

    @property
    def label(self):
        return str(self)

    def __str__(self):
        return self.slug

    def like(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.like()
        return self

    def dislike(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.dislike()
        return self

    def deactivate(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.deactivate()
        return self

    def make_seen(self, user):
        JokeSeen.objects.create(joke=self, user=user)
        return self

    @classmethod
    def get_data_to_export(cls) -> List[Dict]:
        data = [
            {
                'text': item.text,
            } for item in cls.objects.all()
        ]
        return data

    @classmethod
    def validate_data(cls, data):
        return all(cls.is_allowed_to_assign_slug(item['text']) for item in data)

    @classmethod
    def import_data(cls, data):
        for item in data:
            joke, created = Joke.objects.get_or_create(text=item['text'])
            joke.assign_slug()


class JokeSeen(models.Model):
    joke = models.ForeignKey('Joke.Joke', on_delete=models.CASCADE)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    seen_stamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'joke_seen'
        indexes = [
            models.Index(fields=['joke', 'user']),
        ]


class JokeLikeStatus(models.Model):
    is_liked = models.BooleanField(default=None, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joke = models.ForeignKey('Joke.Joke', on_delete=models.CASCADE)

    class Meta:
        db_table = 'joke_like_status'
        indexes = [
            models.Index(fields=['joke', 'user']),
        ]
