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
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", SECRET_KEY)

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
    'words-go-here':{
        'task':'comics.tasks.publish',
        'schedule': timedelta(minutes=10),
    }
}
CELERY_IGNORE_RESULT = True
CELERY_DISABLE_RATE_LIMITS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/django.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'comics': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        },
    },
}

if DEBUG:
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
    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_SECONDS = 60 * 60

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
#    'djrill',
    'datetimewidget',
    'bootstrap3',
    'djorm_fulltext',

    'dashboard',
    'comics',
    'publish',
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

DJANGO_DB_NAME = os.getenv('DJANGO_DB_NAME', 'threepanel')
DJANGO_DB_USER = os.getenv('DJANGO_DB_USER', 'threepanel')
DJANGO_DB_HOST = os.getenv('DJANGO_DB_HOST', 'localhost')
DJANGO_DB_PASSWORD = os.getenv('DJANGO_DB_PASSWORD', 'threepass')
DJANGO_DB_PORT = os.getenv('DJANGO_DB_PORT', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DJANGO_DB_NAME,
        'USER': DJANGO_DB_USER,
        'PASSWORD': DJANGO_DB_PASSWORD,
        'HOST': DJANGO_DB_HOST,
        'PORT': DJANGO_DB_PORT,
    }
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # This is a test key
    #MANDRILL_API_KEY = "b8sBJX8OdA2oXrlhTUlCng"
    #MANDRILL_API_KEY = os.getenv('DJANGO_MANDRILL', MANDRILL_API_KEY)
    pass
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
