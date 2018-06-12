'''
Minimal Django settings required to run tests.
'''
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'django_oaipmh',
)

ROOT_URLCONF = 'django_oaipmh.test_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }
]

# SECRET_KEY = ''
