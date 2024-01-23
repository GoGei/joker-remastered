from typing import List, Dict

from django.db import models
from django.db.models import OuterRef, Subquery, Func, F, Q, Case, When, Value, IntegerField
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.Utils.Mixins.models import CrmMixin, SlugifyMixin, ExportableMixin, ActiveQuerySet


class JokeQuerySet(ActiveQuerySet):
    def ordered(self):
        return self.order_by('slug')

    def annotate_likes(self):
        likes_qub_query = (
            JokeLikeStatus.objects.select_related('joke')
            .filter(joke=OuterRef('pk'), is_liked=True)
            .annotate(count=Func(F('id'), function='Count'))
            .values('count')
        )
        return self.annotate(likes_annotated=Subquery(likes_qub_query))

    def annotate_is_liked_by_user(self, user):
        if not user:
            return self.none()

        likes_qub_query = (
            JokeLikeStatus.objects.select_related('joke')
            .filter(joke=OuterRef('pk'), user=user)
            .values('is_liked')
        )
        return self.annotate(is_liked_by_user_annotated=Subquery(likes_qub_query))

    def __get_seen_joke_ids(self, user):
        if not user:
            return self.none()

        jokes_seen_by_user = JokeSeen.objects.filter(user=user)
        joke_ids = jokes_seen_by_user.values_list('joke_id', flat=True)
        return joke_ids

    def __get_liked_joke_ids(self, user):
        if not user:
            return self.none()

        jokes_seen_by_user = JokeLikeStatus.objects.filter(user=user, is_liked=True)
        joke_ids = jokes_seen_by_user.values_list('joke_id', flat=True)
        return joke_ids

    def seen_by_user(self, user):
        ids = self.__get_seen_joke_ids(user)
        return self.filter(id__in=ids)

    def not_seen_by_user(self, user):
        ids = self.__get_seen_joke_ids(user)
        return self.filter(~Q(id__in=ids))

    def liked_by_user(self, user):
        ids = self.__get_liked_joke_ids(user)
        return self.filter(id__in=ids)

    def not_liked_by_user(self, user):
        ids = self.__get_liked_joke_ids(user)
        return self.filter(~Q(id__in=ids))


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
        self.make_seen(user)
        return self

    def dislike(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.dislike()
        self.make_seen(user)
        return self

    def deactivate(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.deactivate()
        self.make_seen(user)
        return self

    def make_seen(self, user):
        JokeSeen.objects.get_or_create(joke=self, user=user)
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
            models.Index(fields=['is_liked', 'user']),
        ]

    def like(self):
        self.is_liked = True
        self.save(update_fields=['is_liked'])
        return self

    def dislike(self):
        self.is_liked = False
        self.save(update_fields=['is_liked'])
        return self

    def deactivate(self):
        self.is_liked = None
        self.save(update_fields=['is_liked'])
        return self
