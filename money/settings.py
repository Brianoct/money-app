"""
Django settings for money project.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here')  # Use env var for security
# Looks fine; defaults to insecure key if not set in env (safe for local).

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Default to False for production
# Problem: Locally, unless you set the env var DEBUG=True, this is False, hiding errors.
# Fix: For local debugging, set DEBUG = True explicitly.

ALLOWED_HOSTS = ['*']  # Update to your Render domain (e.g., ['your-app-name.onrender.com']) later
# Fine for now; update to ['money-app-1yho.onrender.com'] for Render later.

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'moneyapp',
]
# Looks good; all necessary apps are included.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# Standard middleware setup; Whitenoise is correct for static files.

ROOT_URLCONF = 'money.urls'
# Fine, assuming money/urls.py exists.

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
            ],
        },
    },
]
# Good; APP_DIRS=True means it looks in moneyapp/templates/.

WSGI_APPLICATION = 'money.wsgi.application'
# Correct.

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600  # Render recommends this for PostgreSQL
    )
}
# Locally, this uses SQLite (db.sqlite3). For Render, it needs DATABASE_URL set in env.
# No immediate error here, but ensure db.sqlite3 exists locally.

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# Standard, no issues.

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
# All fine.

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Warning in logs about 'static' not existing is benign unless you need static files now.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Fine.

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'
# Matches your urls.py setup, no problems.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',  # Captures errors like 500
    },
}
# Good for catching 500 errors in logs, but won’t show in browser unless DEBUG=True.