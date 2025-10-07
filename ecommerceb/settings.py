"""
Django settings for ecommerceb project.

For both local (MySQL) and Render (SQLite or DATABASE_URL) environments.
"""

import os
from pathlib import Path
import dj_database_url  # For flexible DB config (Render)
from django.contrib.messages import constants as messages

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-8$h5bbz2%^ah677_fqs+301#-e@%d5a+pq%r%#kaclos)va@(t",
)
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Add your Render app host here
ALLOWED_HOSTS = [
    "Ecom_Admin_Backend.onrender.com",  # ✅ your Render backend app name
    "localhost",
    "127.0.0.1",
]

# --- Installed Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Must be right after SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Place before CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URL and WSGI ---
ROOT_URLCONF = "ecommerceb.urls"
WSGI_APPLICATION = "ecommerceb.wsgi.application"

# --- Templates ---
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

# --- Messages Styling (Bootstrap friendly) ---
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# --- Authentication ---
AUTH_USER_MODEL = "website.AuthUser"
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# --- Databases ---
# Detect Render environment automatically
if os.environ.get("RENDER", None):
    print("⚙️ Using Render/Production Database Settings...")
    DATABASES = {
        "default": dj_database_url.config(
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
            conn_max_age=600,
        )
    }
else:
    print("💻 Using Local MySQL Database Settings...")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "e_commerce",
            "USER": "root",
            "PASSWORD": "Meena@2005",
            "HOST": "localhost",
            "PORT": "3306",
        }
    }

# --- Password Validators ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static & Media Files ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/Media/"
MEDIA_ROOT = BASE_DIR / "Media"

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = True

# --- REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}

# --- Default Primary Key ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
