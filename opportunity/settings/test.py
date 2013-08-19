import os

from .base import *

# When I move this block into base.py this error is generated
#   ImproperlyConfigured: The SECRET_KEY setting must not be empty.
# Leaving it here for now. 
if not six.PY3:
    # boto is required
    from storages.backends.s3boto import S3BotoStorage

    StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
    MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='media')
    DEFAULT_FILE_STORAGE='storages.backends.s3boto.S3BotoStorage'
    # DEFAULT_FILE_STORAGE='opportunity.s3utils.MediaRootS3BotoStorage'

    # To allow django-admin.py collectstatic to automatically put your static 
    # files in your S3 bucket
    STATICFILES_STORAGE = "StaticRootS3BotoStorage"
    # STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test',                      # Or path to database file if using sqlite3.
        'USER': 'jkern',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}


