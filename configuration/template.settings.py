"""
This file generated from the template at configuration/template.settings.py
Django settings for threepanel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

VAGRANT_HOSTNAME = "${VAGRANT_HOSTNAME}"
HOME_DIR = "${HOME}"

ADMINS = ( ("${DJANGO_ADMIN_NAME}", "${DJANGO_ADMIN_EMAIL}"), )

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '${DJANGO_SECRET_KEY}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ${DJANGO_DEBUG}

if DEBUG:
    print("Loading in DEBUG mode!")
else:
    print("Loading in PRODUCTION mode!")

ALLOWED_HOSTS = ['*']

if DEBUG:
    # When we're in debug mode, we don't want any caching to occur
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '/tmp/redis.sock',
        },
    }
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 60 * 60

# CELERY SETTINGS
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

ROOT_URLCONF = '${DJANGO_PROJECT_SLUG}.urls'

WSGI_APPLICATION = '${DJANGO_PROJECT_SLUG}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${DJANGO_PROJECT_SLUG}',
        'USER': '${DJANGO_PROJECT_SLUG}',
        'PASSWORD': '${POSTGRES_DB_PASSWORD}',
        'HOST': 'localhost',
    }
}

if DEBUG:
    SITE_URL = 'http://localhost:18080'
else:
    SITE_URL = "http://${DJANGO_DOMAIN}"

SITE_DOMAIN = "${DJANGO_DOMAIN}"

EMAIL_SUBJECT_PREFIX = '[${DJANGO_PROJECT_SLUG}] '
SERVER_EMAIL = '${DJANGO_ADMIN_EMAIL}'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_ACCESS_KEY_ID = '${AWS_ACCESS_KEY_ID}'
    AWS_SECRET_ACCESS_KEY = '${AWS_SECRET_ACCESS_KEY}'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = False

USE_L10N = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '${HOME}/vagrant_django/nginx/static'

MEDIA_URL = SITE_URL + '/media/upload/'
MEDIA_ROOT = '${HOME}/vagrant_django/nginx/media/upload'

print("Loading local settings")
from ${DJANGO_PROJECT_SLUG}.local_settings import *

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
