from default_settings import *

SECRET_KEY = 'test'
TEST_RUNNER = os.environ.get("TEST_RUNNER", "django.test.runner.DiscoverRunner")

DEBUG = True
API_DOCUMENTATION = False
DEBUG_TOOLBAR = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_TEST_NAME'),
        'USER': os.environ.get('DATABASE_TEST_USER'),
        'PASSWORD': os.environ.get('DATABASE_TEST_PSW'),
        'HOST': os.environ.get('DATABASE_TEST_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_TEST_PORT', 5432),
        'ATOMIC_REQUESTS': True,
    }
}
