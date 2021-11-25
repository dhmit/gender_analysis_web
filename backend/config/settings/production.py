"""

Production settings for gender_analysis_web

"""

import os

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # set in venv activate

ADMINS = ['rahmed@mit.edu']  # Django will email Ryaan on internal server errors

ALLOWED_HOSTS = [
    'dhmitgenderanalysisweb-env.eba-jahuufzr.us-east-2.elasticbeanstalk.com'
]

CORS_ORIGIN_WHITELIST = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}