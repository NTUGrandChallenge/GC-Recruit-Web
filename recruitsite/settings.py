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

    #lbforum
    'el_pagination',
    'easy_thumbnails',
    'constance',
    'constance.backends.database',
    'djangobower',

    'lbforum',
    'lbattachment',
    'lbutils',

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
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'test1',
        
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
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



#lbforum
HOST_URL = ''
MEDIA_URL_ = '/media/'
MEDIA_URL = HOST_URL + MEDIA_URL_

SIGNUP_URL = '/forum/accounts/signup/'
LOGIN_URL = '/forum/accounts/login/'
LOGOUT_URL = '/forum/accounts/logout/'
LOGIN_REDIRECT_URL = '/forum/'
CHANGE_PASSWORD_URL = '/forum/accounts/password/change/'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
      'forbidden_words': ('', 'Forbidden words', str),
}

from django.conf.global_settings import STATICFILES_FINDERS
STATICFILES_FINDERS += (('djangobower.finders.BowerFinder'),)


BOWER_INSTALLED_APPS = (
    'jquery#1.12',
        'markitup#1.1.14',
            'mediaelement#2.22.0',
                'blueimp-file-upload#9.12.5',
                )

BBCODE_AUTO_URLS = True
#add allow tags
HTML_SAFE_TAGS = ['embed']
HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
#add forbid tags
HTML_UNSAFE_TAGS = []
HTML_UNSAFE_ATTRS = []

"""
#default html safe settings
acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
    'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
        'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
            'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
                    'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
                        'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                            'thead', 'tr', 'tt', 'u', 'ul', 'var']
                            acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
                                'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
                                    'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
                                        'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
                                            'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
                                                'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
                                                    'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt',
                                                        'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
                                                            'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
                                                                'usemap', 'valign', 'value', 'vspace', 'width', 'style']
                                                                """
