"""
Django settings for impact project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
# pylint: disable=import-error
from json import load
from pathlib import Path
import os
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import sys
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("IMPACT_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.14', 'impact-suite.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'impactadmin',
    'impactchat',
    'impactclass',

    'jazzmin',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channels',

    'django_react_views'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'impactadmin.middleware.CustomWhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'impact.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'impactadmin.context_processors.react'
            ],
        },
    },
]

WSGI_APPLICATION = 'impact.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'impactdb',
        'USER': 'tommcn',
        # 'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    },
}
if (os.environ.get("RUNNING_DOCKER", None) is not None):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }

print(os.environ.get("DATABASE_URL", None))
if (os.environ.get("DATABASE_URL", None) is not None):
    DATABASES['default'] = dj_database_url.parse(os.environ.get("DATABASE_URL", None), ssl_require=True)
print(DATABASES)

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
# print(DATABASES)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

#  noqa
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-ca'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "impact/static"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
os.makedirs(STATIC_ROOT, exist_ok=True)
for i in STATICFILES_DIRS:
    os.makedirs(STATIC_ROOT, exist_ok=True)


AUTH_USER_MODEL = 'impactadmin.User'
LOGIN_URL = reverse_lazy('impactadmin:login')

ASGI_APPLICATION = 'impact.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', ('127.0.0.1', 6379))],
        },
    },
}

LOCALE_PATHS = BASE_DIR / "locale",
LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

LOGGING = {}
with open('impact/config/logconfig.json') as f:
    LOGGING = load(f)
os.makedirs(BASE_DIR / "logs", exist_ok=True)

JAZZMIN_SETTINGS = {
    'user_avatar': False
}