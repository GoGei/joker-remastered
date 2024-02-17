# Generated by Django 3.2.23 on 2024-01-31 17:24

from django.db import migrations


def admin_forgot_password(apps, schema_editor):
    EmailNotification = apps.get_model('Emailer', 'EmailNotification')

    subject = 'Forgot password'
    email_template_path = 'core/Emailer/templates/admin_forgot_password.html'
    notification, created = EmailNotification.objects.get_or_create(
        slug='admin_forgot_password',
        defaults={
            'subject': subject,
            'email_template_path': email_template_path,
        }
    )

    if not created:
        notification.subject = subject
        notification.email_template_path = email_template_path
        notification.save()


def public_forgot_password(apps, schema_editor):
    EmailNotification = apps.get_model('Emailer', 'EmailNotification')

    subject = 'Forgot password'
    email_template_path = 'core/Emailer/templates/public_forgot_password.html'
    notification, created = EmailNotification.objects.get_or_create(
        slug='public_forgot_password',
        defaults={
            'subject': subject,
            'email_template_path': email_template_path,
        }
    )

    if not created:
        notification.subject = subject
        notification.email_template_path = email_template_path
        notification.save()


class Migration(migrations.Migration):
    dependencies = [
        ('Emailer', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(admin_forgot_password),
        migrations.RunPython(public_forgot_password),
    ]