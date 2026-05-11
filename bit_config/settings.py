from pathlib import Path
from decimal import Decimal
import os
from dotenv import load_dotenv
from django.contrib.messages import constants as messages


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me')
DEBUG =True
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if host.strip()]


SITE_NAME = os.environ.get("SITE_NAME")
REG_NO = os.environ.get("REG_NO")
ADDRESS = os.environ.get("ADDRESS")
EMAIL = os.environ.get("EMAIL")
PHONE = os.environ.get("PHONE")
ADMISSION_FEE = os.environ.get("ADMISSION_FEE")
FAVICON = os.environ.get("FAVICON")
LOGO = os.environ.get("LOGO")
STUDENT_FEE = os.environ.get("STUDENT_FEE")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'dashboard'
]
AUTH_USER_MODEL = 'accounts.User'


MESSAGE_TAGS = {
    messages.SUCCESS: 'success',
    messages.ERROR: 'error',
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bit_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_context',
                'bit_config.context_processors.top_students_footer'
            ],
        },
    },
]

WSGI_APPLICATION = 'bit_config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'khotiyan_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'traditional',
        },
    }
}


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'accounts:login'
LOGIN_URL = 'accounts:login'

ORG_NAME = os.getenv("ORG_NAME", "My System")
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


BKASH_MODE = os.getenv('BKASH_MODE', 'sandbox')

BKASH_APP_KEY = os.getenv('BKASH_APP_KEY','BKASH_APP_KEY')
BKASH_APP_SECRET = os.getenv('BKASH_APP_SECRET','BKASH_APP_SECRET')
BKASH_USERNAME = os.getenv('BKASH_USERNAME','BKASH_USERNAME')
BKASH_PASSWORD = os.getenv('BKASH_PASSWORD','BKASH_PASSWORD')

BKASH_EXTRA_CHARGE_PERCENT = Decimal(os.getenv('BKASH_EXTRA_CHARGE_PERCENT','5'))
BKASH_MIN_DEPOSIT = Decimal(os.getenv('BKASH_MIN_AMOUNT','10'))

