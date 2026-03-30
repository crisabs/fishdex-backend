"""
Base Django settings for Fishdex project.

Contains common settings for all environments.
"""

import os
import sys
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured
from config.service_settings import settings as service_settings

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parents[2]
SECRETS_PATH = "/run/secrets"


# --- Utility to read secrets ---
def read_secret(name: str) -> str | None:
    """Read a secret from the Docker secrets path."""
    try:
        with open(f"{SECRETS_PATH}/{name}") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def read_env_list(name: str, default: str = "") -> list[str]:
    """Read a comma-separated environment variable into a list."""
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


# --- Security ---
DEBUG = service_settings.debug
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or read_secret("django_secret_key")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "insecure-dev-key"
    else:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be configured in non-development environments."
        )
ALLOWED_HOSTS = read_env_list("ALLOWED_HOSTS")

# --- Installed Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "corsheaders",
    # Project apps
    "core",
    "accounts",
    "fishers",
    "fish",
    "inventory",
    "store",
    "capture",
]

# --- Middleware ---
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

# --- URLs & WSGI ---
ROOT_URLCONF = "fishdex.urls"
WSGI_APPLICATION = "fishdex.wsgi.application"

# --- Password Validators ---
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "core.handlers.exception_handler.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# --- JWT Settings ---
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=6),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# --- External Services ---
DJANGO_API_URL = service_settings.django_api_url

# --- Security / Proxy ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# --- Logging ---
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"},
        "json": {
            "format": (
                '{"time": "%(asctime)s", '
                '"level": "%(levelname)s", '
                '"name": "%(name)s", '
                '"message": "%(message)s"}'
            )
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": sys.stdout,
        },
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False}
    },
}

# --- DRF Spectacular ---
SPECTACULAR_SETTINGS = {
    "TITLE": "Fishdex API",
    "DESCRIPTION": "API for Fishdex backend with Django",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY": [{"bearerAuth": []}],
    "COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
}
