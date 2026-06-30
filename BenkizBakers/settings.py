from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# ENV
# ==========================================================
load_dotenv("/home/benkizbakers/.env")

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-in-production"
)

DEBUG = os.getenv("DEBUG", "False") == "True"
DEBUG = True

# ==========================================================
# HOSTS
# ==========================================================
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "benkizbakers.pythonanywhere.com",
    ".vercel.app",
]

# ==========================================================
# INSTALLED APPS
# ==========================================================
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",
    "rest_framework",

    "cloudinary",
    "cloudinary_storage",

    "main.apps.MainConfig",
    "benkizapi",
]

# ==========================================================
# MIDDLEWARE
# ==========================================================
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

# ==========================================================
# TEMPLATES
# ==========================================================
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
    }
]

WSGI_APPLICATION = "BenkizBakers.wsgi.application"

# ==========================================================
# DATABASE
# ==========================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==========================================================
# REST FRAMEWORK
# ==========================================================


# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "benkizapi.authentication.CookieJWTAuthentication",
#     ),

#     "DEFAULT_PARSER_CLASSES": [
#         "rest_framework.parsers.JSONParser",
#         "rest_framework.parsers.FormParser",
#         "rest_framework.parsers.MultiPartParser",
#     ],
# }


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}



# ==========================================================
# JWT
# ==========================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

# ==========================================================
# CLOUDINARY
# ==========================================================
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==========================================================
# CORS
# ==========================================================
CORS_ALLOWED_ORIGINS = [
    "https://benkiz.vercel.app",

    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",

    "https://benkizbakers.pythonanywhere.com",
]


# ==========================================================
# CSRF
# ==========================================================
CSRF_TRUSTED_ORIGINS = [
    "https://benkiz.vercel.app",

    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",

    "https://benkizbakers.pythonanywhere.com",
]

# ==========================================================
# COOKIES
# ==========================================================

if not DEBUG:

    # ==========================================================
    # COOKIES
    # ==========================================================

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_HTTPONLY = True

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_HTTPONLY = False

    SESSION_COOKIE_DOMAIN = None
    CSRF_COOKIE_DOMAIN = None

    # ==========================================================
    # SECURITY
    # ==========================================================
    SECURE_SSL_REDIRECT = True

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    X_FRAME_OPTIONS = "SAMEORIGIN"

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_PATH = "/"
CSRF_COOKIE_PATH = "/"



# ==========================================================
# STATIC
# ==========================================================
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# ==========================================================
# INTERNATIONALIZATION
# ==========================================================
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True

# ==========================================================
# PASSWORD VALIDATORS
# ==========================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"