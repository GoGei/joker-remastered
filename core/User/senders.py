from typing import Optional

from django.conf import settings
from django_hosts import reverse

from core.Emailer.models import EmailNotification
from core.User.models import User
from core.User.redis_services import UserRedisService


class BaseSender(object):
    def __init__(self):
        self.service = UserRedisService()

    def send(self, user: User):
        raise NotImplementedError

    def get(self, key: str) -> Optional[User]:
        user_id = self.service.get(key)
        if not user_id:
            return None
        return User.objects.get(id=user_id)

    def delete(self, key: str):
        return self.service.delete(key)

    @classmethod
    def encoder(cls, user: User, salt: str, *values):
        return user.hashid_encode(salt, *values)


class PublicRegistrationEmailSender(BaseSender):
    def send(self, user: User):
        reverse_url = 'home-register-confirm'
        extra_value = user.hash_str_to_int(reverse_url)
        registration_key = self.encoder(user, settings.HASHID_PUBLIC_SALT, extra_value)
        UserRedisService().set_user_public_registration_key(user, registration_key)

        registration_link = reverse(reverse_url, host='public', kwargs={'key': registration_key})
        context = {
            'email': user.email,
            'registration_link': registration_link,
            'key': registration_key,
        }

        notification = EmailNotification.get_by_slug('public_registration_email')
        notification.send(user.email, context)

        return context

    def get(self, key: str) -> Optional[User]:
        user_id = self.service.get_user_public_registration_by_key(key)
        if not user_id:
            return None
        return User.objects.get(id=user_id)

    def delete(self, key: str):
        return self.service.delete_user_public_registration_key(key)


class PublicForgotPasswordSender(BaseSender):
    def send(self, user: User):
        reverse_url = 'home-forgot-password-confirm'
        extra_value = user.hash_str_to_int(reverse_url)
        activation_key = self.encoder(user, settings.HASHID_PUBLIC_SALT, extra_value)
        UserRedisService().set_user_public_forgot_password_key(user, activation_key)

        activation_link = reverse(reverse_url, host='public', kwargs={'key': activation_key})
        context = {
            'email': user.email,
            'activation_link': activation_link,
            'key': activation_key,
        }

        notification = EmailNotification.get_by_slug('public_forgot_password')
        notification.send(user.email, context)

        return context

    def get(self, key: str) -> Optional[User]:
        user_id = self.service.get_user_public_forgot_password_by_key(key)
        if not user_id:
            return None
        return User.objects.get(id=user_id)

    def delete(self, key: str):
        return self.service.delete_user_public_forgot_password_key(key)


class AdminForgotPasswordSender(BaseSender):
    def send(self, user: User):
        reverse_url = 'admin-forgot-password-confirm'
        extra_value = user.hash_str_to_int(reverse_url)
        activation_key = self.encoder(user, settings.HASHID_ADMIN_SALT, extra_value)
        UserRedisService().set_user_admin_forgot_password_key(user, activation_key)

        activation_link = reverse(reverse_url, host='admin', kwargs={'key': activation_key})
        context = {
            'email': user.email,
            'activation_link': activation_link,
            'key': activation_key,
        }

        notification = EmailNotification.get_by_slug('admin_forgot_password')
        notification.send(user.email, context)

        return context

    def get(self, key: str) -> Optional[User]:
        user_id = self.service.get_user_admin_forgot_password_by_key(key)
        if not user_id:
            return None
        return User.objects.managers().get(id=user_id)

    def delete(self, key: str):
        return self.service.delete_user_admin_forgot_password_key(key)
