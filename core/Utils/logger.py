from django.conf import settings
from django.db.models import TextChoices
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from mongoengine import connection, StringField, DateTimeField, DynamicDocument


class LevelChoices(TextChoices):
    DEBUG = 'debug', _('Debug')
    INFO = 'info', _('Info')
    SUCCESS = 'success', _('Success')
    WARNING = 'warning', _('Warning')
    ERROR = 'error', _('Error')
    CRITICAL = 'critical', _('Critical')
    OBJECT = 'object', _('Object')


class Log(object):
    stamp = DateTimeField(required=True, default=timezone.now)
    description = StringField()
    key = StringField(max_length=255, required=False)
    level = StringField(max_length=255, required=False)

    meta = {"db_alias": settings.MONGODB_LOGGER_ALIAS,
            'dynamic': True,
            'allow_inheritance': False,
            'collection': settings.MONGODB_LOGGER_COLLECTION,
            'indexes': ['stamp']
            }

    @property
    def utcstamp(self):
        return timezone.make_aware(self.stamp, timezone.utc)

    @property
    def localstamp(self):
        return timezone.get_current_timezone().normalize(self.utcstamp)

    def data(self):
        fields = ('key', 'stamp', 'level', 'description')
        return filter(lambda x: x[1] not in fields, self._data.items())


class Logger(object):
    @staticmethod
    def _get_collection(db, collection=None):
        return db[collection or settings.MONGODB_LOGGER_COLLECTION]

    @staticmethod
    def _get_connection():
        return connection.get_db(alias=settings.MONGODB_LOGGER_ALIAS,
                                 reconnect=False)

    def log(self, level: LevelChoices, key: str, description: str, **kwargs):
        db = self._get_connection()
        collection = self._get_collection(db)
        data = {'stamp': timezone.now(),
                'level': level,
                'key': key,
                'description': force_text(description).format(**kwargs)}
        data.update(**kwargs)
        collection.insert_one(data)

    def debug(self, *args, **kwargs):
        return self.log(LevelChoices.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        return self.log(LevelChoices.INFO, *args, **kwargs)

    def success(self, *args, **kwargs):
        return self.log(LevelChoices.SUCCESS, *args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.log(LevelChoices.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        return self.log(LevelChoices.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        return self.log(LevelChoices.CRITICAL, *args, **kwargs)

    def object(self, key: str, description: str, instance, user, level=LevelChoices.OBJECT, **kwargs):
        class_name = instance.__class__.__name__

        kwargs.update({
            '%s_id' % class_name.lower(): instance.id,
            'user_id': str(user.id)
        })

        return self.log(
            level,
            key,
            description,
            obj_type=class_name,
            obj_id=instance.id,
            **kwargs)


class ActivityLog(Log, DynamicDocument):
    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description


def log_qs_to_dict(qs: ActivityLog.objects, fields: tuple = ('key', 'level', 'stamp', 'description')):
    return [
        {
            key: getattr(item, key) for key in fields
        } for item in qs
    ]


log = Logger()
