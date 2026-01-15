"""
Configuración específica para desarrollo.
Ideal para usar con Docker Compose y entorno local.
"""

from .base import *  # noqa: F403, F401
from .base import read_secret, LOGGING
import os
from pathlib import Path

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# --- CORS dinámico desde env_file ---
cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in cors_origins.split(",") if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True

BASE_DIR = Path(__file__).resolve().parents[2]

# --- Base de datos (desde Docker secrets) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": read_secret("pg_db"),
        "USER": read_secret("pg_user"),
        "PASSWORD": read_secret("pg_password"),
        "HOST": "fishdex-postgres-db",
        "PORT": "5432",
    }
}

# --- Permitir cualquier host ---
ALLOWED_HOSTS = ["*"]

# --- LOGGING adicional para desarrollo ---
# Sobrescribimos niveles de log sin tocar variables de entorno internas
# Aseguramos que LOGGING esté definido en base.py (import * lo trae)
if "LOGGING" in globals():
    # loggers nombrados
    if "loggers" in LOGGING:
        LOGGING["loggers"].setdefault("django", {})["level"] = "DEBUG"
        LOGGING["loggers"].setdefault("pokemon", {})["level"] = "DEBUG"
    else:
        LOGGING.setdefault("loggers", {})["django"] = {"level": "DEBUG"}
        LOGGING["loggers"].setdefault("pokemon", {"level": "DEBUG"})

    # logger raíz: debe estar a primer nivel en LOGGING
    if "root" in LOGGING:
        LOGGING["root"]["level"] = "DEBUG"
    else:
        # si por alguna razón no existe, lo creamos con los handlers por defecto
        LOGGING["root"] = {
            "handlers": LOGGING.get("handlers", {}).keys()
            and list(LOGGING["handlers"].keys())
            or ["console"],
            "level": "DEBUG",
        }
else:
    # fallback muy básico si por alguna razón no existe LOGGING
    import logging

    logging.getLogger().setLevel(logging.DEBUG)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# --- Cache desactivada en desarrollo ---
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
