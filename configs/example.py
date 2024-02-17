from default_settings import *

SECRET_KEY = 'super_secret_key'
HASHID_SECRET = 'super_secret_key'
HASHID_ADMIN_SALT = 'admin-extra-salt'
HASHID_PUBLIC_SALT = 'public-extra-salt'
DEBUG = True
API_DOCUMENTATION = True
DEBUG_TOOLBAR = False

TEMPLATES[0]['OPTIONS']['debug'] = True

SITE_URL = 'joker-remastered.local'
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = '4482'
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

DATABASES['default']['PASSWORD'] = 'joker_remastered'

EMAIL_HOST_USER = 'pocket.fridge.team@gmail.com'
DEFAULT_FROM_EMAIL = 'pocket.fridge.team@gmail.com'
EMAIL_HOST_PASSWORD = 'vtshzovfklygyhib'

if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
