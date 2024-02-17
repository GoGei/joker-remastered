from django.conf import settings
from django.utils import timezone
from redis import Redis


class Namespaces(object):
    PUBLIC_USER = 'public-user'
    ADMIN_USER = ' admin-user'


class Actions(object):
    REGISTRATION = 'registration'
    FORGOT_PASSWORD = 'forgot-password'


class RedisKeyFormer(object):
    def __init__(self, separator: str = ':', *args, **kwargs):
        self.separator = separator
        super().__init__(*args, **kwargs)

    def form_key(self, namespace: str, *args):
        return self.separator.join((namespace,) + args)

    def form_public_registration_key(self, registration_key: str) -> str:
        return self.form_key(Namespaces.PUBLIC_USER, Actions.REGISTRATION, registration_key)

    def form_admin_forgot_password_key(self, activation_key: str) -> str:
        return self.form_key(Namespaces.ADMIN_USER, Actions.FORGOT_PASSWORD, activation_key)

    def form_public_forgot_password_key(self, activation_key: str) -> str:
        return self.form_key(Namespaces.PUBLIC_USER, Actions.FORGOT_PASSWORD, activation_key)


class UserRedisService(object):
    def __init__(self):
        self.settings = {
            'host': settings.REDIS_HOST,
            'port': settings.REDIS_PORT,
            'db': settings.REDIS_DB,
        }
        self.key_former = RedisKeyFormer()

    def get(self, key: str):
        with Redis(**self.settings) as r:
            return r.get(key)

    def delete(self, key: str):
        with Redis(**self.settings) as r:
            return r.delete(key)

    def set_user_public_registration_key(self, user, registration_key: str):
        with Redis(**self.settings) as r:
            key = self.key_former.form_public_registration_key(registration_key)
            r.set(key, str(user.id), ex=timezone.timedelta(hours=1))

    def get_user_public_registration_by_key(self, registration_key: str):
        key = self.key_former.form_public_registration_key(registration_key)
        return self.get(key)

    def delete_user_public_registration_key(self, registration_key: str):
        key = self.key_former.form_public_registration_key(registration_key)
        return self.delete(key)

    def set_user_admin_forgot_password_key(self, user, activation_key: str):
        with Redis(**self.settings) as r:
            key = self.key_former.form_admin_forgot_password_key(activation_key)
            r.set(key, str(user.id), ex=timezone.timedelta(hours=1))

    def get_user_admin_forgot_password_by_key(self, activation_key: str):
        key = self.key_former.form_admin_forgot_password_key(activation_key)
        return self.get(key)

    def delete_user_admin_forgot_password_key(self, activation_key: str):
        key = self.key_former.form_admin_forgot_password_key(activation_key)
        return self.delete(key)

    def set_user_public_forgot_password_key(self, user, activation_key: str):
        with Redis(**self.settings) as r:
            key = self.key_former.form_public_forgot_password_key(activation_key)
            r.set(key, str(user.id), ex=timezone.timedelta(hours=1))

    def get_user_public_forgot_password_by_key(self, activation_key: str):
        key = self.key_former.form_public_forgot_password_key(activation_key)
        return self.get(key)

    def delete_user_public_forgot_password_key(self, activation_key: str):
        key = self.key_former.form_public_forgot_password_key(activation_key)
        return self.delete(key)
