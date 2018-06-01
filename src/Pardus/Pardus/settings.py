"""
    Django settings for Pardus project.
"""

#
# Documentation Django sur les réglages d'un projet :
# https://docs.djangoproject.com/fr/2.0/topics/settings/
#
# Les commentaires en anglais sont écrits par défaut lors de la création d'un projet
#

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r#h_v*-gbmua1-^yy-xaom(#41x#n*y8ev0pqi=9m2ftp&detb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Pardus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.get_categories',
                'core.context_processors.website_name',
                'core.context_processors.website_slogan',
            ],
        },
    },
]

WSGI_APPLICATION = 'Pardus.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Fichier statiques (CSS, JavaScript, Images)

#
# Documentation Django sur les fichiers statiques :
# https://docs.djangoproject.com/fr/2.0/howto/static-files/
#

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Fichiers envoyés

#
# Documentation Django sur les fichiers envoyés :
# https://docs.djangoproject.com/fr/2.0/ref/settings/#media-root
# https://docs.djangoproject.com/fr/2.0/ref/settings/#media-url
#

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

# URLs d'authetification

#
# Documentation Django sur les URLs d'authentification :
# https://docs.djangoproject.com/fr/2.0/ref/settings/#login-redirect-url
# https://docs.djangoproject.com/fr/2.0/ref/settings/#login-url
# https://docs.djangoproject.com/fr/2.0/ref/settings/#logout-redirect-url
#

LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "home"
