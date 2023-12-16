from os.path import join, normpath

from decouple import config

from .path import *

# ##### APPLICATION CONFIGURATION #########################
DJANGO_DEFAULT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    "django.contrib.sites",
)

LOCAL_APPS = (
    "apps.chat.apps.ChatConfig",
    "apps.account.apps.AccountConfig",
)

THIRD_PARTY_APPS = (
    "channels",
    "rest_framework",
    "drf_yasg",
)

# these are the apps
DEFAULT_APPS = DJANGO_DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# template stuff
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": PROJECT_TEMPLATES,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ##### SECURITY CONFIGURATION ############################
SECRET_KEY = config("SECRET_KEY", cast=str)

# ##### DJANGO RUNNING CONFIGURATION ######################
# the default WSGI application
WSGI_APPLICATION = "%s.wsgi.application" % SITE_NAME

# the default ASGI application
ASGI_APPLICATION = "%s.asgi.application" % SITE_NAME

print(WSGI_APPLICATION, ASGI_APPLICATION)

# the root URL configuration
ROOT_URLCONF = "%s.urls" % SITE_NAME

# the root URL configuration for websockets
CHANNELS_URLCONF = "%s.urls_channels" % SITE_NAME
