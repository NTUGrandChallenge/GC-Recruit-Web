"""
Django settings for recruitsite project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from recruitsite.secret import DJANGO_SECRET_KEY


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

 #SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'profiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.twitter',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'recruitsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # 'django.template.context_processors.i18n',
                "django.core.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = 'recruitsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'test1',
    #    'NAME': 'gcdb',
    #    'USER': 'gc',
    #    'PASSWORD': 'gc',
    #    'HOST': 'localhost',
    #    'PORT': '',
    #}
     'default': {
         "name": "dc67463fe7ce24dd8bf0d8c18222ce082",
         "host": "198.11.228.48",
         "hostname": "198.11.228.48",
         "port": 5433,
         "user": "u95502d799bde433fb4bc6ec347e15296",
         "username": "u95502d799bde433fb4bc6ec347e15296",
         "password": "pa0ef819988954f238eff6194cc23a75e",
         "uri": "postgres://u95502d799bde433fb4bc6ec347e15296:pa0ef819988954f238eff6194cc23a75e@198.11.228.48:5433/dc67463fe7ce24dd8bf0d8c18222ce082",
     }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#Next, we need to include the Authentication Backend used by allauth:

AUTHENTICATION_BACKENDS = (
    # Default backend -- used to login by username in Django admin
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

#Finally, we are going to set the following parameters to customize the authorization process:

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True
LOGIN_REDIRECT_URL = "/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# TLS Port
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ntuchallenge2016@gmail.com'
# Application Key
EMAIL_HOST_PASSWORD = 'dschooltec'

ADMINS = (
    ('admin1', 'ntuchallenge2016@gmail.com')
    )
MANAGERS = (
    ('manager1', 'ntuchallenge2016@gmail.com')
    )


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/img/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/img'),
]
#STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

LOGIN_REDIRECT_URL = "/index/"

#one-to-one profile user
#AUTH_PROFILE_MODULE = 'profiles.Student'

