from __future__ import annotations

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from core.Utils.Mixins.models import HashableMixin
from core.Emailer.models import EmailNotification


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def managers(self):
        q = Q(is_staff=True) | Q(is_superuser=True)
        return self.filter(q)

    def users(self):
        non_admins_q = Q(is_staff=False, is_superuser=False)
        admins_with_seen_jokes_q = Q(jokeseen__isnull=False)
        q = non_admins_q | admins_with_seen_jokes_q
        return self.prefetch_related('jokeseen_set').filter(q).distinct()

    def active(self):
        return self.filter(is_active=True)


class User(AbstractBaseUser, HashableMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=255, unique=True, db_index=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email or self.id

    @property
    def label(self):
        result = ' '.join(list(filter(lambda x: bool(x), [self.first_name, self.last_name])))
        if not result:
            result = str(self)
        return result

    @property
    def role_label(self):
        if self.is_superuser:
            result = _('Superuser')
        elif self.is_staff:
            result = _('Manager')
        else:
            result = _('User')
        return result
