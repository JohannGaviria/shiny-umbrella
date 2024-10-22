from config.settings.base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'G$9dks!Bf8zQ3*wL%mH7RnX#1p@Vk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
