"""
Configuración base para el proyecto Django.
Contiene los valores comunes para todos los entornos.
"""

import sys
from pathlib import Path
from config.service_settings import settings as service_settings
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parents[2]
SECRETS_PATH = "/run/secrets"


# --- DEBUG ---
# No se define aquí, lo definirá cada entorno
DEBUG = False

# --- CORS ---
# Valores por defecto vacíos, se sobreescriben en cada entorno
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True


# --- Utilidad para leer secretos ---
def read_secret(name):
    try:
        with open(f"{SECRETS_PATH}/{name}") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


# --- REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "core.handlers.exception_handler.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=6),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# --- URLs de servicios ---
DJANGO_API_URL = service_settings.django_api_url

# --- Debug ---
DEBUG = service_settings.debug

# --- Seguridad ---
SECRET_KEY = read_secret("django_secret_key") or "insecure-dev-key"
ALLOWED_HOSTS = ["*"]  # ⚠️ En producción se limitará

# --- Aplicaciones instaladas ---
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
    "accounts",
    "fishers",
]

# --- Middleware ---
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # <-- Debe ir arriba de CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
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

# --- Configuración WSGI ---
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

# --- Internacionalización ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# --- Configuración de clave primaria ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Logging ---


LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": sys.stdout,
        }
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "pokemon": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
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
