from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from celery_run import app
from core.Utils.Logger.logger import log


@app.task(ignore_result=True)
def send_email(subject, body, to_email, from_email=settings.DEFAULT_FROM_EMAIL):
    message = body
    message_html = body

    email_msg = EmailMultiAlternatives(subject,
                                       message,
                                       from_email, to_email)

    email_msg.mixed_subtype = 'related'
    if message_html:
        email_msg.attach_alternative(message_html, "text/html")

    email_msg.send()
    log.info(key='send_email_task', description=_('Email send'))
