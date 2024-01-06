from typing import List, Dict

from django.db import models
from django.db.models import OuterRef, Subquery, Func, F
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.Utils.Mixins.models import CrmMixin, SlugifyMixin, ExportableMixin, ActiveQuerySet


class JokeQuerySet(ActiveQuerySet):
    def annotate_likes(self):
        likes_qub_query = (
            JokeLikeStatus.objects.select_related('joke')
            .filter(joke=OuterRef('pk'), is_liked=True)
            .annotate(count=Func(F('id'), function='Count'))
            .values('count')
        )
        return self.annotate(likes_annotated=Subquery(likes_qub_query))


class Joke(CrmMixin, SlugifyMixin, ExportableMixin):
    SLUGIFY_FIELD = 'text'
    text = models.CharField(max_length=4096)

    objects = JokeQuerySet.as_manager()

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
                'slug': item.slug,
                'is_active': item.is_active
            } for item in cls.objects.all()
        ]
        return data

    @classmethod
    def clear_previous(cls):
        cls.objects.all().archive()

    @classmethod
    def validate_data(cls, data):
        if not data:
            raise ValueError(_('No data to validate'))

        slugs = [item.get('slug') for item in data if item.get('slug')]
        if len(slugs) != len(set(slugs)):
            raise ValueError(_('Please, provide non unique slugs'))

        for item in data:
            text = item.get('text')
            if not text:
                raise ValueError(_('Joke text is required'))

            instance = cls.objects.filter(text=text).first()
            if not cls.is_allowed_to_assign_slug(text, instance):
                raise ValueError(_('Some jokes generate non unique slugs'))

        return data

    @classmethod
    def import_data(cls, data):
        for item in data:
            text = item.get('text')
            slug = item.get('slug')
            is_active = item.get('is_active')

            if not slug:
                joke, created = Joke.objects.get_or_create(text=text)
                joke.assign_slug()
            else:
                joke = cls.objects.filter(slug=slug).first()
                if joke:
                    joke.text = text
                    joke.save()
                else:
                    cls.objects.create(text=text, slug=slug)
                    continue

            if is_active is False:
                joke.archive()
            else:
                joke.restore()

        return cls.objects.all()


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
