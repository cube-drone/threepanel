from datetime import timedelta

# AUTH STUFF
LOGIN_URL = "/dashboard/login"

# TZ
TIME_ZONE = 'America/Vancouver'
USE_TZ = True

FAVICON = 'http://curtis.lassam.net/comics/cube_drone/misc_assets/favicon-1.png'
SITE_TITLE = 'Threepanel'
DEBUG_DOMAIN = 'cube-drone.com'

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djrill',
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s :  %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
        'threepanel':{
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        }
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CELERYBEAT_SCHEDULE = {
    'heartbeat':{
        'task':'dashboard.tasks.heartbeat',
        'schedule': timedelta(minutes=1),
    },
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
