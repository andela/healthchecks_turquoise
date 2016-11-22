import os

if os.environ.get("CIRCLECI") == "true" \
        and os.environ.get("DB") == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'circle_test',
            'USER': 'ubuntu',
            'PASSWORD': '',
            'TEST': {'CHARSET': 'UTF8'},
            'HOST': 'localhost'
        }
    }
