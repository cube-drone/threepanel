"""
Django settings for threepanel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = ( ("Curtis", "curtis@lassam.net"), )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3dypq3o4^%4_7%nzbjo1n_7op524ors3mjurpqa!yh-%jehe8$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# AUTH STUFF
LOGIN_URL = "/dashboard/login"

# TZ
TIME_ZONE = 'America/Vancouver'
USE_TZ = True

CELERYBEAT_SCHEDULE = {
    'publish':{
        'task':'comics.tasks.publish',
        'schedule': timedelta(minutes=10),
    },
    'tidy-subscribers':{
        'task':'publish.tasks.tidy_subscribers',
        'schedule': timedelta(days=1),
    }
}
CELERY_IGNORE_RESULT = True
CELERY_DISABLE_RATE_LIMITS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

# CELERY SETTINGS
BROKER_URL = 'redis+socket:///tmp/redis.sock'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djrill',
    'datetimewidget',
    'bootstrap3',
    'djorm_fulltext',

    'dashboard',
    'comics',
    'publish',
    'pages'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'threepanel.urls'

WSGI_APPLICATION = 'threepanel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'threepanel',
        'USER': 'threepanel',
        'PASSWORD': 'threepass',
        'HOST': 'localhost',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_SUBJECT_PREFIX = "[cube_drone] "
SERVER_EMAIL = "noreply@cubedrone.com"
SITE_URL = "http://localhost:8080"

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = False

USE_L10N = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

try:
    from threepanel.production_settings import *
    print("Loaded production settings!")
except ImportError:
    print("Loading debug settings!")
