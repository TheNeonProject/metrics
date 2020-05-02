import dj_database_url

from project.settings import *  # noqa: F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432'
    }
}

database_url = os.environ.get('DATABASE_URL', None)
if database_url:
    DATABASES['default'] = dj_database_url.parse(
        database_url, conn_max_age=600)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'