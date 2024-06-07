"""
Django settings for zapio project.

Generated by 'django-admin startproject' using Django 2.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


env_path = os.path.join(BASE_DIR, ".env")  # Path(".") / ".env"

load_dotenv(dotenv_path=env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "y8khxyn$m^k*sh*qsk2g7jl261%+e37-!p4_a&xx8j6ucy5e#x"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_swagger",
    "rest_framework_tracking",
    "corsheaders",
    "Configuration",
    "Product",
    "Location",
    "Brands",
    "Outlet",
    "Customers",
    "discount",
    "Orders",
    "History",
    "Notification",
    "backgroundjobs",
    "UserRole",
    "drf_yasg",
    "ZapioApiV2",
    "Subscription",
    "Event",
    "attendance",
    "kitchen",

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "zapio.urls"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CORS_ORIGIN_ALLOW_ALL = True
WSGI_APPLICATION = "zapio.wsgi.application"


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "jp"

# LANGUAGE_CODE = 'de-de'
# LANGUAGES = [
#     ('de')
# ]


TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = (
    ("jp", "Japanese"),
    ("en-us", "English"),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)

JQUERY_URL = True
# JQUERY_URL = False

JET_SIDE_MENU_COMPACT = False






SMS_FROM = os.getenv("SMS_FROM"),
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID"),
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN"),
MSG91_URL = os.getenv("MSG91_URL"),
MSG91_AUTHKEY = os.getenv("MSG91_AUTHKEY"),
MSG91_OTP_FLOWID = os.getenv("MSG91_OTP_FLOWID"),
MSG91_Notification_FLOWID = os.getenv("MSG91_Notification_FLOWID"),
Media_Path = os.getenv("Media_Path")

from celery.schedules import crontab

# CELERY_BEAT_SCHEDULE = {
#     # 'task-hello': {
#     #     'task': 'ZapioApiV2.tasks.print_hello',
#     #     'schedule': crontab(minute="*/1"),
#     # }
#     'task-add': {
#         'task': 'ZapioApiV2..tasks.add',
#         'schedule': 15,
#         'args': (4, 5)
#     },
#     'task-mul': {
#         'task': 'ZapioApiV2.tasks.tasks.mul',
#         'schedule': crontab(minute='*/2'),
#         'args': (4, 5)
#     },
# }
# #0, 0, day_of_month='26'
# CELERY_TIMEZONE = 'Asia/Kolkata'
# CELERY_BROKER_URL = 'amqp://localhost//'
# # Media_Path = "http://192.168.0.112:1234/media/"
# # CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'


from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'task-hello': {
        'task': 'ZapioApiV2.tasks.print_hello',
        'schedule': crontab(minute="*/10", day_of_month="26"),
    },
    'task-report': {
        'task': 'ZapioApiV2.tasks.brand_report',
        'schedule': crontab(minute='*/1'),

    },
    'task-report1': {
        'task': 'ZapioApiV2.tasks.brand_report1',
        'schedule': crontab(minute='*/1'),

    },
    # 'task-email': {
    #     'task': 'backgroundjobs.tasks.daysaleEmail',
    #     'schedule': crontab(minute='*/1'),

    # },
}
#0, 0, day_of_month='26'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BROKER_URL = 'amqp://localhost'

RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.getenv("LOG_FILE"),
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "entities": {
            "handlers": ["file"],
            "propagate": False,
            "level": "INFO",
        },
    },
}

GRAPH_MODELS = {
 'all_applications' : True,
 'group_models' : True,
}