from typing import List, Dict
from slugify import slugify

from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from .exceptions import SlugifyFieldNotSetException


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(archived_stamp__isnull=True)

    def archived(self):
        return self.filter(archived_stamp__isnull=False)

    def archive(self, archived_by=None):
        for item in self:
            item.archive(archived_by)

    def restore(self, restored_by=None):
        for item in self:
            item.restore(restored_by)

    def ordered(self):
        return self.all().order_by('-created_stamp')


class CrmMixin(models.Model):
    created_stamp = models.DateTimeField(default=timezone.now, db_index=True)
    modified_stamp = models.DateTimeField(auto_now=timezone.now)
    archived_stamp = models.DateTimeField(null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')

    objects = ActiveQuerySet.as_manager()

    class Meta:
        abstract = True

    def archive(self, archived_by=None):
        self.archived_stamp = timezone.now()
        if archived_by:
            self.archived_by = archived_by
        self.save()

    def modify(self, modified_by=None):
        self.modified_stamp = timezone.now()
        if modified_by:
            self.modified_by = modified_by
        self.save()

    def restore(self, restored_by=None):
        self.archived_stamp = None
        self.archived_by = None
        self.modify(restored_by)

    def is_active(self) -> bool:
        return not bool(self.archived_stamp)


class SlugifyMixin(models.Model):
    SLUGIFY_FIELD = ''
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def is_allowed_to_assign_slug(cls, value, instance=None):
        slug = slugify(value)
        qs = cls.objects.filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        return not qs.exists()

    def assign_slug(self):
        if not self.SLUGIFY_FIELD:
            raise SlugifyFieldNotSetException('Field for slugify not set!')

        slug = slugify(getattr(self, self.SLUGIFY_FIELD))
        self.slug = slug if len(slug) <= 255 else slug[:255]
        self.save()
        return self


class LikeMixin(models.Model):
    is_liked = models.BooleanField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True

    def like(self):
        self.is_liked = True
        self.save()

    def dislike(self):
        self.is_liked = False
        self.save()

    def deactivate(self):
        self.is_liked = None
        self.save()


class ExportableMixin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_data_to_export(cls) -> List[Dict]:
        raise NotImplementedError

    @classmethod
    def clear_previous(cls):
        raise NotImplementedError

    @classmethod
    def import_data(cls, data):
        raise NotImplementedError

    @classmethod
    @transaction.atomic
    def import_from_data(cls, data):
        cls.clear_previous()
        cls.import_data(data)
        return True
