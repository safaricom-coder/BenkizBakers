# """
# Django settings for BenkizBakers project.
# """

# from pathlib import Path
# import os
# import sys
# from dotenv import load_dotenv

# import cloudinary

# BASE_DIR = Path(__file__).resolve().parent.parent

# # Load .env
# # load_dotenv(BASE_DIR / ".env")  # for offline/local
# load_dotenv("/home/benkizbakers/.env")  # PythonAnywhere


# cloudinary.config(
#     cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
#     api_key=os.environ.get("CLOUDINARY_API_KEY"),
#     api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
#     secure=True,
#     keep_alive=False,
# )

# import cloudinary.api
# import cloudinary.uploader

# # =========================
# # BASIC SETTINGS
# # =========================
# SECRET_KEY = os.environ.get(
#     'SECRET_KEY',
#     'django-insecure-fallback-change-in-production'
# )

# DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "benkizbakers.pythonanywhere.com",
#     ".vercel.app",
# ]

# CSRF_TRUSTED_ORIGINS = [
#     "https://benkizbakers.pythonanywhere.com",
#     "https://benkiz.vercel.app",
    
# ]

# # =========================
# # APPS
# # =========================
# INSTALLED_APPS = [
#     'whitenoise.runserver_nostatic',

#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     'main.apps.MainConfig',
#     'benkizapi',

#     'corsheaders',
#     'rest_framework',

#     'cloudinary',
#     'cloudinary_storage',
# ]

# # =========================
# # CLOUDINARY CONFIG
# # =========================


# CLOUDINARY_STORAGE = {
#     "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
#     "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
#     "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
# }

# STORAGES = {
#     "default": {
#         "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# # Compatibility/support
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# # =========================
# # CORS
# # =========================
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5000",
#     "http://127.0.0.1:5173",
#     "http://127.0.0.1:8000",

#     "https://benkizbakers.pythonanywhere.com",
#     "https://benkiz.vercel.app",
# ]

# SESSION_COOKIE_SAMESITE = 'Lax'
# SESSION_COOKIE_SECURE = False

# CSRF_COOKIE_SAMESITE = 'Lax'
# CSRF_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False

# # =========================
# # REST FRAMEWORK
# # =========================
# REST_FRAMEWORK = {
#     'DEFAULT_PARSER_CLASSES': [
#         'rest_framework.parsers.JSONParser',
#         'rest_framework.parsers.FormParser',
#         'rest_framework.parsers.MultiPartParser',
#     ]
# }

# # =========================
# # MIDDLEWARE
# # =========================
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',

#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',

#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'BenkizBakers.urls'

# # =========================
# # TEMPLATES
# # =========================
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',

#         'DIRS': [BASE_DIR / 'templates'],

#         'APP_DIRS': True,

#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# X_FRAME_OPTIONS = 'SAMEORIGIN'

# WSGI_APPLICATION = 'BenkizBakers.wsgi.application'

# # =========================
# # DATABASE
# # =========================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # =========================
# # PASSWORD VALIDATION
# # =========================
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
#     },
# ]

# # =========================
# # INTERNATIONALIZATION
# # =========================
# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True

# # =========================
# # STATIC FILES
# # =========================
# STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     BASE_DIR / 'static'
# ]

# STATIC_ROOT = BASE_DIR / 'staticfiles'

# # =========================
# # DEFAULT PK
# # =========================
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


"""
Django settings for BenkizBakers project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# =========================
# BASE DIR
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# LOAD ENV FIRST
# =========================
load_dotenv("/home/benkizbakers/.env")  # PythonAnywhere

# =========================
# CLOUDINARY
# =========================
import cloudinary
import cloudinary.api
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
    keep_alive=False,
)



# =========================
# BASIC SETTINGS
# =========================
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-fallback-change-in-production"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "benkizbakers.pythonanywhere.com",
    ".vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://benkizbakers.pythonanywhere.com",
    "https://benkiz.vercel.app",
]

# =========================
# INSTALLED APPS
# =========================
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "main.apps.MainConfig",
    "benkizapi",

    "corsheaders",
    "rest_framework",

    "cloudinary",
    "cloudinary_storage",
]

# =========================
# CLOUDINARY STORAGE
# =========================
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# =========================
# CORS
# =========================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",

    "https://benkizbakers.pythonanywhere.com",
    "https://benkiz.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

# =========================
# COOKIES / CSRF
# =========================
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False

# =========================
# REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ]
}

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "BenkizBakers.urls"

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [BASE_DIR / "templates"],

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

X_FRAME_OPTIONS = "SAMEORIGIN"

WSGI_APPLICATION = "BenkizBakers.wsgi.application"

# =========================
# DATABASE
# =========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# =========================
# DEFAULT PK
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"