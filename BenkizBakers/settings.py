from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta


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
    "http://127.0.0.1:5173"
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


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,

}

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
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "benkizapi.authentication.CookieJWTAuthentication",
    ),

    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
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

# =========================
# COOKIES / CSRF (FIXED FOR PRODUCTION + CROSS DOMAIN VERCEL)
# =========================

SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False

# 🔥 IMPORTANT FIX: allow frontend domain to receive CSRF cookie properly
CSRF_TRUSTED_ORIGINS = [
    "https://benkizbakers.pythonanywhere.com",
    "https://benkiz.vercel.app",
    "http://127.0.0.1:5173",
]

# =========================
# CORS (OK BUT CLEANED ORDER MATTERS)
# =========================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "https://benkiz.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True


# =========================
# SECURITY SETTINGS (FIXED)
# =========================

# SECURE_SSL_REDIRECT = True

# SECURE_PROXY_SSL_HEADER = (
#     "HTTP_X_FORWARDED_PROTO",
#     "https",
# )

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# CRITICAL FIX FOR PYTHONANYWHERE + CROSS DOMAIN COOKIES
CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_DOMAIN = None

# CSRF_COOKIE_DOMAIN = ".pythonanywhere.com"
# SESSION_COOKIE_DOMAIN = ".pythonanywhere.com"