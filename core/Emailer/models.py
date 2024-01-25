from django.db import models
from django.conf import settings
from django.utils import timezone
from django.template import Context, Template
from django.template.loader import render_to_string
from mongoengine import fields, DynamicDocument
from premailer import transform

from core.Utils.Mixins.models import CrmMixin, SlugifyMixin
from .tasks import send_email


class EmailNotification(CrmMixin, SlugifyMixin):
    BASE_TEMPLATE = 'Emailer/base_email_template.html'

    subject = models.CharField(max_length=255)
    email_template_path = models.CharField(max_length=255)

    class Meta:
        db_table = 'email_notifications'

    @classmethod
    def get_by_slug(cls, slug):
        try:
            return cls.objects.active().get(slug=slug)
        except (cls.DoesNotExist, ValueError):
            return None

    def render(self, receiver, context):
        if not context:
            context = {}
        context.update({'receiver': receiver})

        with open(self.email_template_path, 'r') as f:
            message_html = f.read()
        rendered_text = Template(message_html).render(Context(context))
        context.update({'rendered_text': rendered_text})

        base_template = self.BASE_TEMPLATE
        rendered_str = render_to_string(base_template, context)
        result = transform(rendered_str, base_url=settings.SITE)
        return result

    def prepare(self, receiver, context, message_html):
        message = EmailNotificationMessage()
        message.receiver = receiver
        message.notification_id = self.id
        message.subject = self.subject
        message.email_template_path = self.email_template_path
        message.message_html = message_html
        message.context = context
        message.save()
        return message

    def send(self, receiver, context):
        rendered = self.render(receiver, context)
        message = self.prepare(receiver, context, rendered)

        send_email.apply_async(kwargs={
            'subject': self.subject,
            'body': rendered,
            'to_email': [receiver],
        })
        return message


class EmailNotificationMessage(DynamicDocument):
    stamp = fields.DateTimeField(default=timezone.now)
    receiver = fields.DynamicField(index=True)
    notification_id = fields.LongField()
    subject = fields.StringField(null=True)
    email_template_path = fields.StringField(null=True)
    message_html = fields.StringField(null=True)
    context = fields.DictField(null=True)

    meta = {
        "db_alias": settings.MONGODB_NOTIFICATION_ALIAS,
        'allow_inheritance': False,
        'collection': settings.MONGODB_EMAIL_NOTIFICATION_COLLECTION,
        'indexes': [
            'stamp'
        ]
    }

    @property
    def email_notification(self):
        try:
            return EmailNotification.objects.get(id=self.notification_id)
        except (EmailNotification.DoesNotExist, ValueError):
            return None
